from fastapi import APIRouter, HTTPException

from app.models.trabajo_grado import Trabajo_grado
from app.repositories.trabajo_grado_repo import TrabajoGradoRepository


router = APIRouter(
    prefix="/trabajo_grado",
    tags=["Gestión de los trabajos de grado del sistema"]
)

repo = TrabajoGradoRepository()


@router.get("/")
def obtener_trabajos_de_grado():
    return repo.obtenerTrabajosGrados()


@router.get("/{id_trabajo_grado}")
def obtener_trabajos_de_grado_por_id(id_trabajo_grado: int):

    trabajo_grado = repo.obtenerTrabajoGradoPorId(
        id_trabajo_grado
    )

    if trabajo_grado is None:
        raise HTTPException(
            status_code=404,
            detail="Trabajo de grado no encontrado"
        )

    return trabajo_grado


@router.post("/")
def crear_trabajo_grado(trabajo_grado: Trabajo_grado):

    return repo.crearTrabajoGrado(trabajo_grado)


@router.put("/{id_trabajo_grado}")
def actualizar_trabajo_grado(
    id_trabajo_grado: int,
    trabajo_grado: Trabajo_grado
):

    actualizado = repo.actualizarTrabajoGrado(
        id_trabajo_grado,
        trabajo_grado
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Trabajo de grado no encontrado"
        )

    return {
        "Mensaje": "Trabajo de grado actualizado exitosamente"
    }


@router.delete("/{id_trabajo_grado}", status_code=204)
def eliminar_trabajo(id_trabajo_grado: int):
    try:
        eliminado = repo.eliminarTrabajoGrado(id_trabajo_grado)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if not eliminado:
        raise HTTPException(status_code=404, detail="Trabajo de grado no encontrado")