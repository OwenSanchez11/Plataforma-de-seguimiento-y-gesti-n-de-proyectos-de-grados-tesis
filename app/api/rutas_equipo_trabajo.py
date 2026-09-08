from fastapi import APIRouter, HTTPException

from app.models.equipo_trabajo import (
    EquipoTrabajoCrear,
    ActualizarEquipoTrabajo
)
from app.repositories.equipo_trabajo_repo import EquipoTrabajoRepository


router = APIRouter(
    prefix="/equipo-trabajo",
    tags=["Gestión de equipos de trabajo"]
)

repo = EquipoTrabajoRepository()


@router.get("/")
def obtener_equipos_trabajo():

    return repo.obtenerEquiposTrabajo()


@router.get("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def obtener_equipo_trabajo_por_id(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int
):

    equipo = repo.obtenerEquipoTrabajoPorId(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto
    )

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail="Equipo de trabajo no encontrado"
        )

    return equipo


@router.post("/")
def crear_equipo_trabajo(equipo: EquipoTrabajoCrear):

    return repo.crearEquipoTrabajo(equipo)


@router.put("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def actualizar_equipo_trabajo(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int,
    equipo: ActualizarEquipoTrabajo
):

    actualizado = repo.actualizarEquipoTrabajo(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto,
        equipo
    )

    if actualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Equipo de trabajo no encontrado"
        )

    return {
        "mensaje": "Equipo de trabajo actualizado correctamente"
    }


@router.delete("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def eliminar_equipo_trabajo(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int
):

    eliminado = repo.eliminarEquipoTrabajo(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto
    )

    if eliminado is None:
        raise HTTPException(
            status_code=404,
            detail="Equipo de trabajo no encontrado"
        )

    return {
        "mensaje": "Equipo de trabajo eliminado correctamente"
    }
