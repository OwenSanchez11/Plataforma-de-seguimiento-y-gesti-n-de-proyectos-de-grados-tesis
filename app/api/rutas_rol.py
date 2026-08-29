from fastapi import APIRouter, HTTPException
from app.models.rol import Rol
from app.repositories.rol_repo import RolRepository


router = APIRouter(prefix="/rol", tags=["Gestión de roles del sistema"])
repo = RolRepository()


@router.get("/")
def obtener_roles():
    return repo.obtenerRoles()

@router.get("/{id_rol}")
def obtener_rol_por_id(id_rol: int):
    rol = repo.obtenerRolPorId(id_rol)
    if not rol:
        raise HTTPException(status_code= 404, detail= "Rol no encontrado")
    return rol

@router.post("/")
def crear_rol(rol: Rol):
    nuevo_id_rol = repo.crearRol(rol)
    return {"Mensaje ": "Rol registrado exitosamente", "id": nuevo_id_rol}

@router.put("/{id_rol}")
def actualizar_roles(id_rol: int, rol: Rol):
    actualizarRol = repo.actualizarRol(id_rol, rol)
    
    return {
            "Mensaje": "Rol actualizado exitosamente",
            "actualizado": actualizarRol
        }

@router.delete("/{id_rol}")
def eliminar_rol(id_rol: int):
    rolEliminado = repo.eliminarRol(id_rol)
    if not rolEliminado:
        raise HTTPException(status_code= 404, detail= "Rol no encontrado")
    return {"Mensaje": "Rol eliminado correctamente"}  