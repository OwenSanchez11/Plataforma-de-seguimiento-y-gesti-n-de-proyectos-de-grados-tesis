from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.models.modulos_por_rol import Modulo_rol
from app.repositories.modulos_rol_repo import ModuloPorRolRepository

router = APIRouter(prefix="/modulos_rol", tags=["Gestión de modulos por rol"])
repo = ModuloPorRolRepository()



@router.get("/")
def obtener_modulos_rol():
    return repo.obtenerModuloRol()


@router.get("/{id_modulo_rol}")
def obtener_modulo_rol_por_id(id_modulo_rol: int):
    modulo_rol = repo.obtenerModuloRolPorId(id_modulo_rol)
    
    if not modulo_rol: 
        raise HTTPException(status_code= 404, detail= "Modulo por rol no encontrado")
    return modulo_rol



@router.post("/")
def crear_modulo_por_rol(modulo: Modulo_rol):
    nuevo_modulo_rol = repo.crearModuloPorRol(modulo)
    return {
        "Mensaje ": "Modulo por rol registrado exitosamente", "id": nuevo_modulo_rol
    }



@router.put("/{id_modulo_rol}")
def actualizar_modulo_rol(id_modulo_rol: int, modulo: Modulo_rol):
    actualizado = repo.actualizarModuloRol(id_modulo_rol, modulo)
    
    return {
        "Mensaje": "Usuario actualizado exitosamente",
        "actualizado": actualizado
    }
    
    

@router.delete("/{id_modulo_rol}")
def eliminar_modulo_rol(id_modulo_rol: int):
    exito = repo.eliminarModuloRol(id_modulo_rol)
    if not exito:
        raise HTTPException(status_code=404, detail="Modulo por rol no encontrado")
    return {"Mensaje": "MOdulo por rol eliminado correctamente"}  
