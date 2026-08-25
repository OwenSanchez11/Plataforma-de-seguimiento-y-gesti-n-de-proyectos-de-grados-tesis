from fastapi import APIRouter, HTTPException

from app.models.entrega import CrearEntrega
from app.models.entrega import ActualizarEntrega

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
def crear_entrega(entrega: CrearEntrega):

    nuevo_id_entrega = repo.crearEntrega(entrega)

    return {
        "Mensaje": "Entrega registrada exitosamente",
        "id": nuevo_id_entrega
    }


@router.put("/{id_entrega}")
def actualizar_entrega(
    id_entrega: int,
    entrega: ActualizarEntrega
):

    actualizarEntrega = repo.actualizarEntrega(
        id_entrega,
        entrega
    )

    if not actualizarEntrega:
        raise HTTPException(
            status_code=404,
            detail="Entrega no encontrada"
        )

    return {
        "Mensaje": "Entrega actualizada exitosamente",
        "actualizado": actualizarEntrega
    }


@router.delete("/{id_entrega}")
def eliminar_entrega(id_entrega: int):

    entregaEliminada = repo.eliminarEntrega(id_entrega)

    if not entregaEliminada:
        raise HTTPException(
            status_code=404,
            detail="Entrega no encontrada"
        )

    return {
        "Mensaje": "Entrega eliminada correctamente"
    }