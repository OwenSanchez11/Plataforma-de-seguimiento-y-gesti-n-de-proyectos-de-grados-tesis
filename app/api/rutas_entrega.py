from fastapi import APIRouter, HTTPException

from app.models.entrega import Entrega

from app.repositories.entrega_repo import EntregaRepository


router = APIRouter(

    prefix="/entrega",

    tags=["Gestión de entregas"]

)

repo = EntregaRepository()


@router.get("/")
def obtener_entregas():

    return repo.obtenerEntregas()


@router.get("/{id_entrega}")
def obtener_entrega_por_id(id_entrega: int):

    entrega = repo.obtenerEntregaPorId(id_entrega)

    if not entrega:

        raise HTTPException(
            status_code=404,
            detail="Entrega no encontrada"
        )

    return entrega


@router.post("/")
def crear_entrega(entrega: Entrega):

    nuevo_id_entrega = repo.crearEntrega(entrega)

    return {
        "Mensaje": "Entrega registrada exitosamente",
        "id_entrega": nuevo_id_entrega
    }


@router.put("/{id_entrega}")
def actualizar_entrega(
    id_entrega: int,
    entrega: Entrega
):

    actualizada = repo.actualizarEntrega(
        id_entrega,
        entrega
    )

    if not actualizada:

        raise HTTPException(
            status_code=404,
            detail="Entrega no encontrada"
        )

    return {
        "Mensaje": "Entrega actualizada exitosamente"
    }


@router.delete("/{id_entrega}")
def eliminar_entrega(id_entrega: int):

    eliminada = repo.eliminarEntrega(id_entrega)

    if not eliminada:

        raise HTTPException(
            status_code=404,
            detail="Entrega no encontrada"
        )

    return {
        "Mensaje": "Entrega eliminada correctamente"
    }