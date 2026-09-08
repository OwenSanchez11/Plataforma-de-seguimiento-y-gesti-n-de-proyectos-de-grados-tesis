from fastapi import APIRouter, HTTPException

from app.models.equipo_trabajo import (
    EquipoTrabajo

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


@router.get("/{id_equipo}")
def obtener_equipo_trabajo_por_id(
    id_equipo: int
):

    equipo = repo.obtenerEquipoTrabajoPorId(
       id_equipo
    )

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail="Equipo de trabajo no encontrado"
        )

    return equipo


@router.post("/")
def crear_equipo_trabajo(equipo: EquipoTrabajo):
    return repo.crearEquipoTrabajo(equipo)


@router.put("/{id_equipo}")
def actualizar_equipo_trabajo(
    id_equipo: int,
    equipo: EquipoTrabajo
):

    actualizado = repo.actualizarEquipoTrabajo(
        id_equipo,
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


@router.delete("/{id_equipo}")
def eliminar_equipo_trabajo(
    id_equipo: int
):

    eliminado = repo.eliminarEquipoTrabajo(
        id_equipo
    )

    if eliminado is None:
        raise HTTPException(
            status_code=404,
            detail="Equipo de trabajo no encontrado"
        )

    return {
        "mensaje": "Equipo de trabajo eliminado correctamente"
    }