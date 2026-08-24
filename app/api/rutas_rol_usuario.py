from fastapi import APIRouter, HTTPException
from app.models.rol_usuario import CrearRelacionUsuarioRol
from app.models.rol_usuario import ActualizarRelacionRolYUsuario
from app.repositories.rol_usuario_repo import RolUsuarioRepository

router = APIRouter(prefix="/rol_usuario", tags=["Gestión de los roles asignados a cada usuario del sistema"])
repo = RolUsuarioRepository()


@router.get("/")
def obtener_roles_usuarios(): 
    return repo.obtenerRolesYUsuario()

@router.get("/{id_rol_usuario}")
def obtener_roles_usuarios_por_id(id_rol_usuario: int):
    rolUsuario = repo.obtenerRolYUsuarioPorId(id_rol_usuario)
    
    if not rolUsuario:
        raise HTTPException(status_code= 404, detail="Usuario y rol no encontrado")
    return rolUsuario

@router.post("/")
def crear_relacion_usuario_rol(rol_usuario: CrearRelacionUsuarioRol):
    nuevo_rol_usuario = repo.crearRelacionUsuarioRol(rol_usuario)
    return {"Mensaje ": "relación registrada exitosamente", "id": nuevo_rol_usuario}

@router.put("/{id_rol_usuario}")
def actualizar_rol_del_usuario(id_rol: int, rol_usuario: ActualizarRelacionRolYUsuario):
    actualizarRelacionRolUsuario = repo.actualizarRelacionUsuarioRol(id_rol, rol_usuario)
    
    return {
                "Mensaje": "Rol actualizado exitosamente",
                "actualizado": actualizarRelacionRolUsuario
            }
    
@router.delete("/{id_rol_usuario}")
def eliminar_relacion_rol_usuario(id_rol_usuario: int):
    eliminarRolUsuario = repo.eliminarRelacionRolUsuario(id_rol_usuario)
    if not eliminarRolUsuario:
        raise HTTPException(status_code= 404, detail= "Relacion no encontrada")
    return {"Mensaje": "Relación eliminada correctamente"}  
    