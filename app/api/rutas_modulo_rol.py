from fastapi import APIRouter, HTTPException

from app.models.modulo_rol import ModuloRol, ActualizarModuloRol
from app.repositories.modulo_rol_repo import ModuloRolRepository


router = APIRouter(
    prefix="/modulo-rol",
    tags=["Gestión de Módulos por Rol"]
)

repo = ModuloRolRepository()


@router.get("/")
def obtener_modulos_rol():

    return repo.obtenerModulosRol()


@router.get("/{id_modulo_rol}")
def obtener_modulo_rol_por_id(id_modulo_rol: int):

    modulo_rol = repo.obtenerModuloRolPorId(id_modulo_rol)

    if modulo_rol is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo por rol no encontrado"
        )

    return modulo_rol


@router.post("/")
def crear_modulo_rol(modulo_rol: ModuloRol):

    return repo.crearModuloRol(modulo_rol)


@router.put("/{id_modulo_rol}")
def actualizar_modulo_rol(
    id_modulo_rol: int,
    modulo_rol: ActualizarModuloRol
):

    actualizado = repo.actualizarModuloRol(
        id_modulo_rol,
        modulo_rol
    )

    if actualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo por rol no encontrado"
        )

    return {
        "mensaje": "Módulo por rol actualizado exitosamente"
    }


@router.delete("/{id_modulo_rol}")
def eliminar_modulo_rol(id_modulo_rol: int):

    eliminado = repo.eliminarModuloRol(id_modulo_rol)

    if eliminado is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo por rol no encontrado"
        )

    return {
        "mensaje": "Módulo por rol eliminado correctamente"
    }