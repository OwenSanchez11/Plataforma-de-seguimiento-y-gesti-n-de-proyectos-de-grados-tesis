import os
import re
from contextlib import closing
from datetime import datetime, timezone
from typing import Annotated
from urllib.parse import quote
from uuid import uuid4

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile

from app.core.database import Database
from app.core.security import admin, coordinador, docente, estudiante, solo_roles


router = APIRouter(prefix="/avances", tags=["Documentos de avances"])
MAX_PDF = 10 * 1024 * 1024


def almacenamiento():
    cuenta = os.getenv("R2_ACCOUNT_ID")
    bucket = os.getenv("R2_BUCKET")
    acceso = os.getenv("R2_ACCESS_KEY_ID")
    secreto = os.getenv("R2_SECRET_ACCESS_KEY")
    if not all((cuenta, bucket, acceso, secreto)):
        raise HTTPException(503, "El almacenamiento de entregables aún no está configurado.")

    cliente = boto3.client(
        "s3",
        endpoint_url=f"https://{cuenta}.r2.cloudflarestorage.com",
        aws_access_key_id=acceso,
        aws_secret_access_key=secreto,
        region_name="auto",
        config=Config(
            signature_version="s3v4",
            connect_timeout=5,
            read_timeout=20,
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        ),
    )
    return cliente, bucket


def obtener_avance(cursor, id_avance, sesion, bloquear=False):
    bloqueo = "FOR UPDATE OF a" if bloquear else ""
    cursor.execute(
        f"""
        SELECT a.id_avance, a.id_trabajo_grado, a.estado, a.dictamen, a.ruta_archivo,
               a.nombre_archivo
        FROM avances a
        JOIN trabajo_grado t ON t.id_trabajo_grado = a.id_trabajo_grado
        JOIN usuario u ON u.id_user = %s AND u.estado = true AND u.id_rol = %s
        WHERE a.id_avance = %s
        AND (
            u.id_rol = %s
            OR (u.id_rol = %s AND u.id_carrera = t.id_carrera)
            OR (u.id_rol IN (%s, %s) AND EXISTS (
                SELECT 1 FROM equipo_trabajo e
                WHERE e.id_trabajo_grado = t.id_trabajo_grado
                AND e.id_usuario = u.id_user AND e.estado = true
            ))
        )
        {bloqueo}
        """,
        (sesion["sub"], sesion["id_rol"], id_avance, admin, coordinador, estudiante, docente),
    )
    avance = cursor.fetchone()
    if not avance:
        raise HTTPException(404, "Avance no encontrado o sin acceso.")
    return avance


def prefijo(avance):
    return f'entregables/{avance["id_trabajo_grado"]}/{avance["id_avance"]}/'


def leer_pdf(archivo):
    nombre = re.split(r"[/\\]", archivo.filename or "")[-1]
    nombre = re.sub(r"[\x00-\x1f\x7f]", "", nombre).strip()
    if not nombre.lower().endswith(".pdf") or len(nombre) > 200:
        raise HTTPException(415, "Selecciona un archivo PDF con nombre de hasta 200 caracteres.")
    contenido = archivo.file.read(MAX_PDF + 1)
    if len(contenido) > MAX_PDF:
        raise HTTPException(413, "El PDF debe pesar como máximo 10 MB.")
    if not re.match(rb"%PDF-[12]\.\d(?:\r|\n)", contenido) or not contenido.rstrip().endswith(b"%%EOF"):
        raise HTTPException(415, "El archivo seleccionado no es un PDF válido.")

    return nombre, contenido


def guardar_en_r2(cliente, bucket, clave, contenido):
    try:
        cliente.put_object(Bucket=bucket, Key=clave, Body=contenido, ContentType="application/pdf")
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(502, "No se pudo guardar el PDF en el almacenamiento.") from exc


@router.post("/trabajo/{id_trabajo_grado}/archivo", status_code=201)
def crear_avance_con_archivo(
    id_trabajo_grado: int,
    archivo: UploadFile,
    titulo: Annotated[str, Form()],
    descripcion: Annotated[str, Form()],
    sesion: dict = Depends(solo_roles(estudiante)),
):
    titulo, descripcion = titulo.strip(), descripcion.strip()
    if not titulo or not descripcion:
        raise HTTPException(422, "Completa el título y la descripción del avance.")
    nombre, contenido = leer_pdf(archivo)

    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO avances (id_trabajo_grado, subido_por, titulo, descripcion,
                                 nombre_archivo, tamano_bytes, fecha_entrega,
                                 numero_version, estado, dictamen)
            SELECT e.id_trabajo_grado, u.id_user, %s, %s, %s, %s, %s, 1, true, %s
            FROM usuario u
            JOIN equipo_trabajo e ON e.id_usuario = u.id_user AND e.estado = true
            WHERE u.id_user = %s AND u.estado = true AND u.id_rol = %s
              AND e.id_trabajo_grado = %s
            LIMIT 1
            RETURNING id_avance, id_trabajo_grado
            """,
            (titulo, descripcion, nombre, len(contenido), datetime.now(timezone.utc),
             "en revisión", sesion["sub"], estudiante, id_trabajo_grado),
        )
        avance = cursor.fetchone()
        if not avance:
            raise HTTPException(404, "Trabajo de grado no encontrado o sin acceso.")

        cliente, bucket = almacenamiento()
        clave = f"{prefijo(avance)}{uuid4().hex}.pdf"
        cursor.execute(
            "UPDATE avances SET ruta_archivo = %s WHERE id_avance = %s RETURNING *",
            (clave, avance["id_avance"]),
        )
        resultado = cursor.fetchone()
        guardar_en_r2(cliente, bucket, clave, contenido)
        conexion.commit()
        return resultado


@router.post("/{id_avance}/archivo")
def cargar_archivo(
    id_avance: int, archivo: UploadFile, sesion: dict = Depends(solo_roles(estudiante))
):
    nombre, contenido = leer_pdf(archivo)
    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        avance = obtener_avance(cursor, id_avance, sesion, bloquear=True)
        if not avance["estado"] or (avance["dictamen"] or "").lower() == "aprobado":
            raise HTTPException(409, "Este avance ya no admite entregas.")
        cliente, bucket = almacenamiento()
        clave = f"{prefijo(avance)}{uuid4().hex}.pdf"

        cursor.execute(
            """
            UPDATE avances
            SET nombre_archivo = %s, ruta_archivo = %s, tamano_bytes = %s,
                fecha_entrega = %s, subido_por = %s, dictamen = NULL,
                numero_version = COALESCE(numero_version, 0) + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id_avance = %s
            RETURNING id_avance, nombre_archivo, ruta_archivo, tamano_bytes,
                      fecha_entrega, numero_version, dictamen
            """,
            (nombre, clave, len(contenido), datetime.now(timezone.utc), sesion["sub"], id_avance),
        )
        resultado = cursor.fetchone()
        guardar_en_r2(cliente, bucket, clave, contenido)
        conexion.commit()
        return resultado


@router.get("/{id_avance}/archivo")
def descargar_archivo(
    id_avance: int, respuesta: Response,
    sesion: dict = Depends(solo_roles(estudiante, docente, coordinador, admin)),
):
    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        avance = obtener_avance(cursor, id_avance, sesion)
    clave = avance["ruta_archivo"] or ""
    if not re.fullmatch(rf"{re.escape(prefijo(avance))}[a-f0-9]{{32}}\.pdf", clave):
        raise HTTPException(404, "Este avance no tiene un PDF almacenado.")

    cliente, bucket = almacenamiento()
    nombre = quote(avance["nombre_archivo"] or "entregable.pdf", safe="")
    try:
        url = cliente.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket, "Key": clave,
                "ResponseContentDisposition": f"attachment; filename*=UTF-8''{nombre}",
            },
            ExpiresIn=60,
        )
    except (BotoCoreError, ClientError) as exc:
        raise HTTPException(502, "No se pudo preparar la descarga del PDF.") from exc
    respuesta.headers["Cache-Control"] = "no-store"
    return {"url": url}
