from fastapi import APIRouter, HTTPException

from app.models.avances import Avances

from app.repositories.avances_repo import AvancesRepository


router = APIRouter(
    prefix="/avances",
    tags=["Gestión de avances"]
)

repo = AvancesRepository()


@router.get("/")
def obtener_avances():

    return repo.obtenerAvances()


@router.get("/{id_avances}")
def obtener_avances_por_id(id_avances: int):

    avances = repo.obtenerAvancesPorId(id_avances)

    if not avances:
        raise HTTPException(
            status_code=404,
            detail="Avances no encontrado"
        )

    return avances


@router.post("/")
def crear_avances(avances: Avances):

    nuevo_id_avances = repo.crearAvances(avances)

    return {
        "Mensaje": "Avances registrado exitosamente",
        "id_avances": nuevo_id_avances
    }


@router.put("/{id_avances}")
def actualizar_avances(
    id_avances: int,
    avances: Avances
):

    actualizado = repo.actualizarAvances(
        id_avances,
        avances
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Avances no encontrado"
        )

    return {
        "Mensaje": "Avances actualizado exitosamente"
    }


@router.delete("/{id_avances}")
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