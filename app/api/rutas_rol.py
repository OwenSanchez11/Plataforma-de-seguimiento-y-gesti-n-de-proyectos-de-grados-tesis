from fastapi import APIRouter, HTTPException

from app.models.rol import Rol
from app.repositories.rol_repo import RolRepository


router = APIRouter(
    prefix="/rol",
    tags=["Gestión de roles del sistema"]
)

repo = RolRepository()


@router.get("/")
def obtener_roles():
    return repo.obtenerRoles()


@router.get("/{id_rol}")
def obtener_rol_por_id(id_rol: int):

    rol = repo.obtenerRolPorId(id_rol)

    if rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return rol


@router.post("/")
def crear_rol(rol: Rol):

    return repo.crearRol(rol)


@router.put("/{id_rol}")
def actualizar_rol(id_rol: int, rol: Rol):

    actualizado = repo.actualizarRol(id_rol, rol)

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {
        "Mensaje": "Rol actualizado exitosamente"
    }


@router.delete("/{id_rol}")
def eliminar_rol(id_rol: int):

    eliminado = repo.eliminarRol(id_rol)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {
        "Mensaje": "Rol eliminado correctamente"
    }