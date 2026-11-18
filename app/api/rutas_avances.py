from contextlib import closing

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import admin, coordinador, docente, solo_roles

from app.api.rutas_archivos_avances import obtener_avance
from app.core.database import Database
from app.models.avances import Avances
from app.repositories.avances_repo import AvancesRepository


router = APIRouter(
    prefix="/avances",
    tags=["Gestión de avances"],
)

repo = AvancesRepository()


@router.get("/")
def obtener_avances(id_trabajo_grado: int | None = None):
    return repo.obtenerAvances(id_trabajo_grado)


@router.get("/trabajo/{id_trabajo_grado}")
def avance_por_trabajo(id_trabajo_grado: int):
    return repo.obtenerAvancePorTrabajo(id_trabajo_grado)


@router.get("/{id_avance}")
def obtener_avance_por_id(id_avance: int):
    avance = repo.obtenerAvancesPorId(id_avance)

    if avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    return avance


@router.post("/")
def crear_avance(avance: Avances):
    nuevo_id_avance = repo.crearAvances(avance)

    if nuevo_id_avance is None:
        raise HTTPException(status_code=400, detail="No fue posible registrar el avance")

    return {
        "mensaje": "Avance registrado exitosamente",
        "id_avance": nuevo_id_avance
    }


@router.put("/{id_avance}")
def actualizar_avance(
    id_avance: int, avance: Avances, sesion: dict = Depends(solo_roles(admin, coordinador, docente))
):
    es_docente = sesion["id_rol"] == docente
    if es_docente:
        with closing(Database().getConnection()) as conexion, conexion.cursor() as cursor:
            actual = obtener_avance(cursor, id_avance, sesion)
        if avance.id_trabajo_grado != actual["id_trabajo_grado"]:
            raise HTTPException(403, "El docente no puede reasignar un avance.")

    actualizado = repo.actualizarAvances(id_avance, avance, verificar_archivo=es_docente)
    if not actualizado and es_docente:
        raise HTTPException(409, "La entrega cambió. Actualiza la lista antes de guardar el dictamen.")

    if not actualizado:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    return {"mensaje": "Avance actualizado exitosamente"}


@router.delete("/{id_avance}", dependencies=[Depends(solo_roles(admin, coordinador))])
def eliminar_avance(id_avance: int):
    eliminado = repo.eliminarAvances(id_avance)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Avance no encontrado")

    return {"mensaje": "Avance eliminado correctamente"}
