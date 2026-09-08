from fastapi import APIRouter, HTTPException

from app.models.retroalimentaciones import Retroalimentacion
from app.repositories.retroalimentacion_repo import RetroalimentacionesRepository


router = APIRouter(
    prefix="/retroalimentaciones",
    tags=["Gestión de retroalimentaciones"]
)

repo = RetroalimentacionesRepository()


@router.get("/")
def obtener_retroalimentaciones():
    return repo.obtenerRetroalimentacion()


@router.get("/{id_retroalimentacion}")
def obtener_retroalimentacion_por_id(id_retroalimentacion: int):

    retroalimentacion = repo.obtenerRetroalimentacionPorId(
        id_retroalimentacion
    )

    if retroalimentacion is None:
        raise HTTPException(
            status_code=404,
            detail="Retroalimentación no encontrada"
        )

    return retroalimentacion


@router.post("/")
def crear_retroalimentacion(
    retroalimentacion: Retroalimentacion
):

    return repo.crearRetroalimentacion(retroalimentacion)


@router.put("/{id_retroalimentacion}")
def actualizar_retroalimentacion(
    id_retroalimentacion: int,
    retroalimentacion: Retroalimentacion
):

    actualizado = repo.actualizarRetroalimentacion(
        id_retroalimentacion,
        retroalimentacion
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Retroalimentación no encontrada"
        )

    return {
        "Mensaje": "Retroalimentación actualizada exitosamente"
    }


@router.delete("/{id_retroalimentacion}")
def eliminar_retroalimentacion(id_retroalimentacion: int):

    eliminado = repo.eliminarRetroalimentacion(
        id_retroalimentacion
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Retroalimentación no encontrada"
        )

    return {
        "Mensaje": "Retroalimentación eliminada correctamente"
    }