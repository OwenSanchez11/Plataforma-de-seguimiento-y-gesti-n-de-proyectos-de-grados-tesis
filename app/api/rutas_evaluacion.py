from fastapi import APIRouter, HTTPException, Depends

from app.core.security import estudiante, solo_roles
from app.repositories.equipo_trabajo_repo import EquipoTrabajoRepository
from app.models.evaluacion import Evaluacion

from app.repositories.evaluacion_repo import EvaluacionRepository


router = APIRouter(
    prefix="/evaluaciones",
    tags=["Gestión de evaluaciones"]
)

repo = EvaluacionRepository()
equipo_repo = EquipoTrabajoRepository()


@router.get("/")
def obtener_evaluaciones(id_carrera: int | None = None, id_facultad:int | None=None):

    return repo.obtenerEvaluaciones(id_carrera, id_facultad)

@router.get("/mi-trabajo")
def obtener_mis_evaluaciones(usuario=Depends(solo_roles(estudiante))):
    id_user = int(usuario["sub"])

    datos = equipo_repo.obtenerTrabajoPorEstudiante(id_user)
    if datos is None:
        raise HTTPException(
            status_code=404,
            detail="No tienes un trabajo de grado asignado"
        )

    id_trabajo_grado = datos["trabajo"]["id_trabajo_grado"]
    return repo.obtenerEvaluacionPorTrabajo(id_trabajo_grado)


@router.get("/{id_evaluacion}")
def obtener_evaluacion_por_id(id_evaluacion: int):

    evaluacion = repo.obtenerEvaluacionPorId(id_evaluacion)

    if evaluacion is None:

        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return evaluacion


@router.post("/")
def crear_evaluacion(evaluacion: Evaluacion):

    return repo.crearEvaluacion(evaluacion)


@router.put("/{id_evaluacion}")
def actualizar_evaluacion(
    id_evaluacion: int,
    evaluacion: Evaluacion
):

    actualizado = repo.actualizarEvaluacion(
        id_evaluacion,
        evaluacion
    )

    if not actualizado:

        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return {
        "mensaje": "Evaluación actualizada correctamente"
    }


@router.delete("/{id_evaluacion}")
def eliminar_evaluacion(id_evaluacion: int):

    eliminado = repo.eliminarEvaluacion(id_evaluacion)

    if not eliminado:

        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return {
        "mensaje": "Evaluación eliminada correctamente"
    }
