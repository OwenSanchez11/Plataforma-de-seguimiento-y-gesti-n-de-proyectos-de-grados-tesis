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

    if not evaluacion:

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

    resultado = repo.actualizarEvaluacion(
        id_evaluacion,
        evaluacion
    )

    if resultado.get("mensaje") == "Evaluación no encontrada":

        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return resultado


@router.delete("/{id_evaluacion}")
def eliminar_evaluacion(id_evaluacion: int):

    resultado = repo.eliminarEvaluacion(id_evaluacion)

    if resultado.get("mensaje") == "Evaluación no encontrada":

        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return resultado