from fastapi import APIRouter, HTTPException

from app.models.permiso import Permiso

from app.repositories.permiso_repo import PermisoRepository


router = APIRouter(

    prefix="/permisos",

    tags=["Gestión de permisos"]

)

repo = PermisoRepository()


@router.get("/")
def obtener_permisos():

    return repo.obtenerPermisos()


@router.get("/{id_permiso}")
def obtener_permiso_por_id(id_permiso: int):

    permiso = repo.obtenerPermisoPorId(id_permiso)

    if not permiso:

        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return permiso


@router.post("/")
def crear_permiso(permiso: Permiso):

    return repo.crearPermiso(permiso)


@router.put("/{id_permiso}")
def actualizar_permiso(
    id_permiso: int,
    permiso: Permiso
):

    resultado = repo.actualizarPermiso(
        id_permiso,
        permiso
    )

    if resultado.get("mensaje") == "Permiso no encontrado":

        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return resultado


@router.delete("/{id_permiso}")
def eliminar_permiso(id_permiso: int):

    resultado = repo.eliminarPermiso(id_permiso)

    if resultado.get("mensaje") == "Permiso no encontrado":

        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado"
        )

    return resultado