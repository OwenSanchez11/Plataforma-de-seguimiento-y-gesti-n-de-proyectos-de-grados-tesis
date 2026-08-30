from fastapi import APIRouter, HTTPException

from app.models.facultad import FacultadCrear, ActualizarFacultad
from app.repositories.facultad_repo import FacultadRepository


router = APIRouter(
    prefix="/facultades",
    tags=["Gestión de facultades"]
)

repo = FacultadRepository()


@router.get("/")
def obtener_facultades():
    return repo.obtenerFacultades()


@router.get("/{id_facultad}")
def obtener_facultad_por_id(id_facultad: int):

    facultad = repo.obtenerFacultadPorId(id_facultad)

    if facultad is None:
        raise HTTPException(
            status_code=404,
            detail="Facultad no encontrada"
        )

    return facultad


@router.post("/")
def crear_facultad(facultad: FacultadCrear):

    return repo.crearFacultad(facultad)


@router.put("/{id_facultad}")
def actualizar_facultad(
    id_facultad: int,
    facultad: ActualizarFacultad
):

    actualizado = repo.actualizarFacultad(
        id_facultad,
        facultad
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Facultad no encontrada"
        )

    return {
        "mensaje": "Facultad actualizada correctamente"
    }


@router.delete("/{id_facultad}")
def eliminar_facultad(id_facultad: int):

    eliminado = repo.eliminarFacultad(id_facultad)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Facultad no encontrada"
        )

    return {
        "mensaje": "Facultad eliminada correctamente"
    }