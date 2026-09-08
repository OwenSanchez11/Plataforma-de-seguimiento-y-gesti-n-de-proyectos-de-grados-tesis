from fastapi import APIRouter, HTTPException

from app.models.asignacion import Asignacion
from app.repositories.asignacion_repo import AsignacionRepository


router = APIRouter(
    prefix="/asignaciones",
    tags=["Gestión de asignaciones"]
)

repo = AsignacionRepository()


@router.get("/")
def obtener_asignaciones():
    return repo.obtenerAsignaciones()


@router.get("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def obtener_asignacion_por_id(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int
):
    asignacion = repo.obtenerAsignacionPorId(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto
    )

    if asignacion is None:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    return asignacion


@router.post("/")
def crear_asignacion(asignacion: Asignacion):
    return repo.crearAsignacion(asignacion)


@router.put("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def actualizar_asignacion(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int,
    asignacion: Asignacion
):
    actualizado = repo.actualizarAsignacion(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto,
        asignacion
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    return {
        "Mensaje": "Asignación actualizada correctamente"
    }


@router.delete("/{id_trabajo_grado}/{id_usuario}/{id_rol_proyecto}")
def eliminar_asignacion(
    id_trabajo_grado: int,
    id_usuario: int,
    id_rol_proyecto: int
):
    eliminado = repo.eliminarAsignacion(
        id_trabajo_grado,
        id_usuario,
        id_rol_proyecto
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Asignación no encontrada"
        )

    return {
        "Mensaje": "Asignación eliminada correctamente"
    }