from fastapi import APIRouter, HTTPException
from app.models.retroalimentaciones import Retroalimentacion
from app.repositories.retroalimentacion_repo import RetroalimentacionesRepository

router = APIRouter(prefix="/retroalimentaciones", tags=["Gestión de las retroalimentaciones dadas a cada entrega de los trabajos de grados del sistema"])
repo = RetroalimentacionesRepository()

@router.get("/")
def obtener_retro(): 
    return repo.obtenerRetroalimentacion()

@router.get("/{id_retroalimentacion}")
def obtener_retroalimentaciones_id(id_retroalimentacion: int):
    retroalimentacion = repo.obtenerRetroalimentacionPorId(id_retroalimentacion)
    
    if not retroalimentacion:
        raise HTTPException(status_code= 404, detail="retroalimentacion no encontrada")
    return retroalimentacion



@router.post("/")
def crear_retroalimentacion(retroalimentacion: Retroalimentacion):
    nueva_retroalimentacion = repo.crearRetroalimentacion(retroalimentacion)
    return {"Mensaje ": " retroalimentacion registrada exitosamente", "id": nueva_retroalimentacion}


@router.put("/{id_retroalimentacion}")
def actualizar_retroalimentacion(id_retroalimentacion: int, retroalimentacion: Retroalimentacion):
    actualizarRetroalimentacion = repo.actualizarRetroalimentacion(id_retroalimentacion, retroalimentacion)
    
    return {
                "Mensaje": "Retroalimentación actualizada exitosamente",
                "actualizado": actualizarRetroalimentacion
            }
    

@router.delete("/{id_retroalimentacion}")
def eliminar_retroalimentacion(id_retroalimentacion: int):
    eliminar_retroalimentacion = repo.eliminarRetroalimentacion(id_retroalimentacion)
    if not eliminar_retroalimentacion:
        raise HTTPException(status_code= 404, detail= "retroalimentación no encontrada")
    return {"Mensaje": "Retroalimentación eliminada correctamente"}  