from fastapi import APIRouter, HTTPException

from app.models.hito import CrearHito
from app.models.hito import ActualizarHito

from app.repositories.hito_repo import HitoRepository


router = APIRouter(
    prefix="/hitos",
    tags=["Gestión de hitos"]
)

repo = HitoRepository()


@router.get("/")
def obtener_hitos():
    return repo.obtenerHitos()


@router.get("/{id_hito}")
def obtener_hito_por_id(id_hito: int):

    hito = repo.obtenerHitoPorId(id_hito)

    if not hito:
        raise HTTPException(
            status_code=404,
            detail="Hito no encontrado"
        )

    return hito


@router.post("/")
def crear_hito(hito: CrearHito):

    nuevo_id_hito = repo.crearHito(hito)

    return {
        "Mensaje": "Hito registrado exitosamente",
        "id": nuevo_id_hito
    }


@router.put("/{id_hito}")
def actualizar_hito(
    id_hito: int,
    hito: ActualizarHito
):

    actualizado = repo.actualizarHito(
        id_hito,
        hito
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Hito no encontrado"
        )

    return {
        "Mensaje": "Hito actualizado exitosamente",
        "actualizado": actualizado
    }


@router.delete("/{id_hito}")
def eliminar_hito(id_hito: int):

    eliminado = repo.eliminarHito(id_hito)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Hito no encontrado"
        )

    return {
        "Mensaje": "Hito eliminado correctamente"
    }