import json
import os
import smtplib
import ssl
from base64 import b64encode
from collections import Counter
from contextlib import closing
from datetime import date
from email.headerregistry import Address
from email.message import EmailMessage
from email.errors import HeaderParseError
from io import BytesIO
from typing import Annotated, Literal
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, PositiveInt, field_validator, model_validator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer

from app.core.database import Database
from app.core.security import admin, coordinador, solo_roles


router = APIRouter(prefix="/reportes/trabajos-grado", tags=["Reportes"])
NOMBRE_PDF = "trabajos-de-grado.pdf"
ASUNTO_REPORTE = "GradosTrack | Reporte de trabajos de grado"
TEXTO_REPORTE = "Adjuntamos el reporte de trabajos de grado que solicitaste en GradosTrack."


class FiltrosReporte(BaseModel):
    id_carrera: PositiveInt | None = None
    estado_tramite: Literal["En proceso", "Finalizado", "Cancelado"] | None = None
    desde: date | None = None
    hasta: date | None = None

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.desde and self.hasta and self.desde > self.hasta:
            raise ValueError("La fecha inicial debe ser anterior o igual a la fecha final.")
        return self


class EnvioReporte(FiltrosReporte):
    destinatario: str | None = None

    @field_validator("destinatario")
    @classmethod
    def validar_destinatario(cls, valor):
        if valor is None:
            return valor
        correo = valor.strip()
        try:
            direccion = Address(addr_spec=correo)
        except (ValueError, HeaderParseError) as exc:
            raise ValueError("Escribe un correo con formato correcto.") from exc
        if (
            not direccion.username or not direccion.domain or len(correo) > 254
            or not correo.isascii() or direccion.addr_spec != correo
        ):
            raise ValueError("Escribe un correo con formato correcto.")
        return correo


def obtener_usuario(usuario: Annotated[dict, Depends(solo_roles(admin, coordinador))]):
    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_rol, id_carrera, email FROM usuario WHERE id_user = %s AND estado = true",
            (usuario["sub"],),
        )
        cuenta = cursor.fetchone()

    if not cuenta or cuenta["id_rol"] != usuario["id_rol"]:
        raise HTTPException(403, "La cuenta ya no tiene acceso a los reportes.")
    if cuenta["id_rol"] == coordinador and cuenta["id_carrera"] is None:
        raise HTTPException(403, "Tu cuenta debe tener una carrera asignada para generar reportes.")
    return cuenta


UsuarioReporte = Annotated[dict, Depends(obtener_usuario)]


@router.get("/carreras")
def listar_carreras(usuario: UsuarioReporte):
    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        if usuario["id_rol"] == coordinador:
            cursor.execute(
                "SELECT id_carrera, nombre_carrera FROM carrera WHERE id_carrera = %s",
                (usuario["id_carrera"],),
            )
        else:
            cursor.execute("SELECT id_carrera, nombre_carrera FROM carrera ORDER BY nombre_carrera")
        return cursor.fetchall()


def consultar_trabajos(filtros: FiltrosReporte, usuario: dict):
    id_carrera = filtros.id_carrera
    if usuario["id_rol"] == coordinador:
        if id_carrera is not None and id_carrera != usuario["id_carrera"]:
            raise HTTPException(403, "Solo puedes generar reportes de tu carrera.")
        id_carrera = usuario["id_carrera"]

    condiciones = []
    parametros = []
    for condicion, valor in (
        ("t.id_carrera = %s", id_carrera),
        ("t.estado_tramite = %s", filtros.estado_tramite),
        ("t.fecha_inicio >= %s", filtros.desde),
        ("t.fecha_inicio <= %s", filtros.hasta),
    ):
        if valor is not None:
            condiciones.append(condicion)
            parametros.append(valor)
    where = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
        cursor.execute(
            f"""SELECT t.id_trabajo_grado, t.titulo, c.nombre_carrera, f.nombre_facultad,
                       t.estado_tramite, t.fecha_inicio
                FROM trabajo_grado t
                LEFT JOIN carrera c ON c.id_carrera = t.id_carrera
                LEFT JOIN facultad f ON f.id_facultad = c.id_facultad
                {where}
                ORDER BY t.fecha_inicio DESC NULLS LAST, t.id_trabajo_grado""",
            parametros,
        )
        return cursor.fetchall()


@router.get("/vista-previa")
def visualizar_reporte(
    filtros: Annotated[FiltrosReporte, Query()], usuario: UsuarioReporte, respuesta: Response
):
    respuesta.headers["Cache-Control"] = "no-store"
    return consultar_trabajos(filtros, usuario)


def dibujar_pagina(pdf, documento):
    ancho, alto = documento.pagesize
    pdf.saveState()
    pdf.setFillColor(colors.HexColor("#142857"))
    pdf.rect(0, alto - 49, ancho, 49, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(documento.leftMargin, alto - 30, "GradosTrack")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(ancho - documento.rightMargin, alto - 30, "Trabajos de grado")

    pdf.setStrokeColor(colors.HexColor("#cad7e8"))
    pdf.line(documento.leftMargin, 43, ancho - documento.rightMargin, 43)
    pdf.setFillColor(colors.HexColor("#334155"))
    pdf.setFont("Helvetica", 9)
    pdf.drawString(documento.leftMargin, 27, "Sistema de seguimiento de trabajos de grado")
    pdf.drawRightString(ancho - documento.rightMargin, 27, f"Página {documento.page}")
    pdf.restoreState()


def generar_pdf(trabajos):
    archivo = BytesIO()
    estilos = getSampleStyleSheet()
    estilos["Title"].textColor = colors.HexColor("#142857")
    estilos["Heading2"].textColor = colors.HexColor("#194997")
    estilos["Normal"].fontName = "Helvetica"
    estilos["Normal"].fontSize = 9
    totales = Counter(fila["estado_tramite"] or "Sin estado" for fila in trabajos)
    contenido = [
        Paragraph("Reporte de trabajos de grado", estilos["Title"]),
        Paragraph(f"Total de trabajos: {len(trabajos)}", estilos["Heading2"]),
    ]
    for estado, total in sorted(totales.items()):
        contenido.append(Paragraph(f"{escape(estado)}: {total}", estilos["Normal"]))
    contenido.append(Spacer(1, 14))

    if trabajos:
        datos = [["Título", "Carrera", "Facultad", "Estado", "Fecha de inicio"]]
        for fila in trabajos:
            datos.append([
                Paragraph(escape(str(fila[campo] or "—")), estilos["Normal"])
                for campo in ("titulo", "nombre_carrera", "nombre_facultad", "estado_tramite", "fecha_inicio")
            ])
        contenido.append(LongTable(
            datos, colWidths=[169, 101, 101, 67, 83], repeatRows=1, splitInRow=1,
            style=[
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#194997")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#edf4ff"), colors.white]),
            ],
        ))
    else:
        contenido.append(Paragraph("No hay trabajos para los filtros seleccionados.", estilos["Normal"]))

    SimpleDocTemplate(
        archivo, pagesize=A4, leftMargin=29, rightMargin=29, topMargin=64, bottomMargin=54,
        title="Trabajos de grado | GradosTrack",
    ).build(contenido, onFirstPage=dibujar_pagina, onLaterPages=dibujar_pagina)
    return archivo.getvalue()


@router.get("/pdf", response_class=Response)
def descargar_pdf(filtros: Annotated[FiltrosReporte, Query()], usuario: UsuarioReporte):
    return Response(
        generar_pdf(consultar_trabajos(filtros, usuario)),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{NOMBRE_PDF}"', "Cache-Control": "no-store"},
    )


def enviar_por_brevo(clave: str, remitente: str, destinatario: str, pdf: bytes):
    solicitud = Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps({
            "sender": {"email": remitente},
            "to": [{"email": destinatario}],
            "subject": ASUNTO_REPORTE,
            "textContent": TEXTO_REPORTE,
            "attachment": [{"name": NOMBRE_PDF, "content": b64encode(pdf).decode("ascii")}],
        }).encode("utf-8"),
        headers={"api-key": clave, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(solicitud, timeout=20):
            pass
    except OSError as exc:
        raise HTTPException(502, "Brevo no pudo confirmar el envío del correo.") from exc


@router.post("/envios", status_code=204)
def enviar_reporte(filtros: EnvioReporte, usuario: UsuarioReporte):
    clave_brevo = os.getenv("BREVO_API_KEY")
    if clave_brevo:
        remitente_brevo = os.getenv("BREVO_FROM")
        if not remitente_brevo:
            raise HTTPException(503, "Falta configurar el remitente de Brevo.")
        destinatario = filtros.destinatario or usuario["email"]
        if not destinatario:
            raise HTTPException(409, "Indica un correo de destino.")
        pdf = generar_pdf(consultar_trabajos(filtros, usuario))
        enviar_por_brevo(clave_brevo, remitente_brevo, destinatario, pdf)
        return

    servidor = os.getenv("SMTP_HOST")
    remitente = os.getenv("SMTP_FROM")
    cuenta_smtp = os.getenv("SMTP_USER")
    clave_smtp = os.getenv("SMTP_PASSWORD")
    if not servidor or not remitente or bool(cuenta_smtp) != bool(clave_smtp):
        raise HTTPException(503, "El servicio de correo aún no está configurado.")

    destinatario = filtros.destinatario or usuario["email"]
    if not destinatario:
        raise HTTPException(409, "Tu cuenta no tiene un correo registrado.")

    pdf = generar_pdf(consultar_trabajos(filtros, usuario))
    mensaje = EmailMessage()
    mensaje["Subject"] = ASUNTO_REPORTE
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje.set_content(TEXTO_REPORTE)
    mensaje.add_attachment(pdf, maintype="application", subtype="pdf", filename=NOMBRE_PDF)
    try:
        puerto = int(os.getenv("SMTP_PORT", "587"))
        contexto = ssl.create_default_context()
        cliente = (
            smtplib.SMTP_SSL(servidor, puerto, timeout=20, context=contexto)
            if puerto == 465 else smtplib.SMTP(servidor, puerto, timeout=20)
        )
        with cliente as smtp:
            if puerto != 465:
                smtp.starttls(context=contexto)
            if cuenta_smtp:
                smtp.login(cuenta_smtp, clave_smtp)
            smtp.send_message(mensaje, from_addr=remitente, to_addrs=[destinatario])
    except (OSError, ValueError) as exc:
        raise HTTPException(502, "No se pudo enviar el correo. Inténtalo de nuevo.") from exc
