from fastapi import APIRouter, HTTPException

from app.models.rol_proyecto import Rol_proyecto
from app.repositories.rol_proyecto_repo import RolProyectoRepository


router = APIRouter(
    prefix="/roles-proyecto",
    tags=["Gestión de roles de proyecto"]
)

repo = RolProyectoRepository()


@router.get("/")
def obtener_roles_proyecto():
    return repo.obtenerRolesProyecto()


@router.get("/{id_rol_proyecto}")
def obtener_rol_proyecto_por_id(id_rol_proyecto: int):

    rol = repo.obtenerPorId(id_rol_proyecto)

    if rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol de proyecto no encontrado"
        )

    return rol


@router.post("/")
def crear_rol_proyecto(rol_proyecto: Rol_proyecto):

    return repo.crearRolProyecto(rol_proyecto)


@router.put("/{id_rol_proyecto}")
def actualizar_rol_proyecto(id_rol_proyecto: int, rol_proyecto: Rol_proyecto):

    actualizado = repo.actualizarRolProyecto(
        id_rol_proyecto,
        rol_proyecto
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Rol de proyecto no encontrado"
        )

    return {
        "Mensaje": "Rol de proyecto actualizado exitosamente"
    }


@router.delete("/{id_rol_proyecto}")
def eliminar_rol_proyecto(id_rol_proyecto: int):

    eliminado = repo.eliminarRolProyecto(id_rol_proyecto)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Rol de proyecto no encontrado"
        )

    return {
        "Mensaje": "Rol de proyecto eliminado correctamente"
    }