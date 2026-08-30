from fastapi import APIRouter, HTTPException

from app.models.avances import CrearAvances
from app.models.avances import ActualizarAvances

from app.repositories.avances_repo import AvancesRepository


router = APIRouter(
    prefix="/avances",
    tags=["Gestión de avances"]
)

repo = AvancesRepository()


@router.get("/")
def obtener_avances():
    return repo.obtenerHitos()


@router.get("/{id_hito}")
def obtener_avances_por_id(id_avances: int):

    hito = repo.obtenerHitoPorId(id_avances)

    if not hito:
        raise HTTPException(
            status_code=404,
            detail="Hito no encontrado"
        )

    return hito


@router.post("/")
def crear_avances(avances: CrearAvances):

    nuevo_id_avances = repo.crearHito(avances)

    return {
        "Mensaje": "Hito registrado exitosamente",
        "id": nuevo_id_avances
    }


@router.put("/{id_avances}")
def actualizar_hito(
    id_avances: int,
    avances: ActualizarAvances
):

    actualizado = repo.actualizarAvances(
        id_avances,
        avances
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Hito no encontrado"
        )

    return {
        "Mensaje": "Avances actualizado exitosamente",
        "actualizado": actualizado
    }


@router.delete("/{id_hito}")
def eliminar_avances(id_avances: int):

    eliminado = repo.eliminarAvances(id_avances)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Avances no encontrado"
        )

    return {
        "Mensaje": "Avances eliminado correctamente"
    }