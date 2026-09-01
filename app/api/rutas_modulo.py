from fastapi import APIRouter, HTTPException

from app.models.modulo import Modulo

from app.repositories.modulos_repo import ModuloRepository



router = APIRouter(

    prefix="/modulos",

    tags=["Gestión de Modulos"]

)

repo = ModuloRepository()


@router.get("/")
def obtener_modulos():
    return repo.obtenerModulos()


@router.get("/{id_modulo}")
def obtener_modulos_por_id(id_modulo: int):
    
    modulo = repo.obtenerModuloId(id_modulo)
    
    if not modulo:
        
        raise HTTPException(
            status_code=404,
            detail="Modulo no encontrada"
        )

    return modulo

@router.post("/")
def crear_modulo(modulo: Modulo):
    
    return repo.crearModulo(modulo)

@router.put("/{id_modulo}")
def actualizar_modulo(id_modulo: int, modulo: Modulo):
    
    resultado = repo.actualizarModulo(id_modulo, modulo)
    
    return {
        "Mensaje": "Modulo actualizado exitosamente",
        "Actualizado": resultado
    }


@router.delete("/{id_modulo}")
def eliminar_modulo(id_modulo: int): 
    exito = repo.eliminarModulo(id_modulo)
    if not exito:
        raise HTTPException(status_code=404, detail="Modulo no encontrado")
    return {"Mensaje": "Modulo eliminado correctamente"}   