from fastapi import APIRouter, HTTPException

from app.models.evaluacion import Evaluacion

from app.repositories.evaluacion_repo import EvaluacionRepository


router = APIRouter(
    prefix="/evaluaciones",
    tags=["Gestión de evaluaciones"]
)

repo = EvaluacionRepository()


@router.get("/")
def obtener_evaluaciones():

    return repo.obtenerEvaluaciones()


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