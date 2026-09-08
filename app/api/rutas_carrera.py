from fastapi import APIRouter, HTTPException

from app.models.carrera import Carrera
from app.repositories.carrera_repo import CarreraRepository


router = APIRouter(
    prefix="/carreras",
    tags=["Gestión de carreras"]
)

repo = CarreraRepository()


@router.get("/")
def obtener_carreras():
    return repo.obtenerCarreras()


@router.get("/{id_carrera}")
def obtener_carrera_por_id(id_carrera: int):

    carrera = repo.obtenerCarreraPorId(id_carrera)

    if carrera is None:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    return carrera


@router.post("/")
def crear_carrera(carrera: Carrera):

    return repo.crearCarrera(carrera)


@router.put("/{id_carrera}")
def actualizar_carrera(
    id_carrera: int,
    carrera: Carrera
):

    actualizado = repo.actualizarCarrera(
        id_carrera,
        carrera
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    return {
        "Mensaje": "Carrera actualizada correctamente"
    }


@router.delete("/{id_carrera}")
def eliminar_carrera(id_carrera: int):

    eliminado = repo.eliminarCarrera(id_carrera)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    return {
        "Mensaje": "Carrera eliminada correctamente"
    }