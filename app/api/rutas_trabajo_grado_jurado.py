from fastapi import APIRouter, HTTPException
from app.repositories.trabajo_grado_jurado_repo import TrabajoGradoJuradoRepository
from app.models.trabajo_grado_jurado import Actualizar_trabajo_grado_jurado
from app.models.trabajo_grado_jurado import Crear_trabajo_grado_jurado

router = APIRouter(prefix="/trabajoGradoJurado", tags=["Gestión de los trabajos de grados asignados a los jurados"])
repo = TrabajoGradoJuradoRepository()


@router.get("/")
def obtener_trabajos_de_grado_por_jurado():
    return repo.obtenerTrabajosPorJurado()


@router.get("/{id_trabajo_grado_jurado}")
def obtener_trabajo_grado_por_jurado_por_id(id_trabajo_grado_jurado: int):
    Trabajo_grado_jurado = repo.obtenerTrabajoGradoPorJuradoPorId(id_trabajo_grado_jurado)
    
    if not Trabajo_grado_jurado:
        raise HTTPException(status_code= 404, detail="trabajo de grado por jurado no encontrado")
    return Trabajo_grado_jurado


@router.post("/")
def crear_trabajo_grado_por_jurado(trabajo_grado_jurado: Crear_trabajo_grado_jurado):
    nuevo_trabajo_grado_por_jurado = repo.crearRelacionTrabajoGradoPorJurado(trabajo_grado_jurado)
    return {"Mensaje ": "Trabajo de grado asignado exitosamente", "id: ": nuevo_trabajo_grado_por_jurado}



@router.put("/{id_trabajo_grado_jurado}")
def actualizar_trabajo_grado_por_jurado(id_trabajo_grado_jurado: int, trabajo_grado_juado: Actualizar_trabajo_grado_jurado):
    Actualizar_trabajo_grado_jurado = repo.actualizarTrabajoGradoPorJurado(id_trabajo_grado_jurado, trabajo_grado_juado)
    
    return {
        "Mensaje": "Asignación del trabajo actualizado exitosamente",
        "Actualizado": Actualizar_trabajo_grado_jurado
    }
    

@router.delete("/{id_trabajo_grado_jurado}")
def eliminar_trabajo_grado_por_jurado(id_trabajo_grado_jurado: int): 
    eliminar_trabajo_por_jurado = repo.eliminarTrabajoGradoPorJurado(id_trabajo_grado_jurado)
    if not eliminar_trabajo_por_jurado:
        raise HTTPException(status_code= 404, detail= "trabajo de grado por jurado no fue encontrado")
    return {"Mensaje": "Trabajo de grado por jurado eliminado correctamente"}

