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


@router.get("/{id_avance}")
def obtener_avance_por_id(id_avance: int):

    avance = repo.obtenerAvancesPorId(id_avance)

    if not avance:
        raise HTTPException(
            status_code=404,
            detail="Avance no encontrado"
        )

    return avance


@router.post("/")
def crear_avance(avance: Avances):

    nuevo_id_avance = repo.crearAvances(avance)

    return {
        "Mensaje": "Avance registrado exitosamente",
        "id_avance": nuevo_id_avance
    }


@router.put("/{id_avance}")
def actualizar_avance(
    id_avance: int,
    avance: Avances
):

    actualizado = repo.actualizarAvances(
        id_avance,
        avance
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Avance no encontrado"
        )

    return {
        "Mensaje": "Avance actualizado exitosamente"
    }


@router.delete("/{id_avance}")
def eliminar_avance(id_avance: int):

    eliminado = repo.eliminarAvances(id_avance)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Avance no encontrado"
        )

    return {
        "Mensaje": "Avance eliminado correctamente"
    }