from fastapi import APIRouter, HTTPException
from app.models.trabajo_grado_director import Crear_trabajo_grado_director
from app.models.trabajo_grado_director import Actualizar_trabajo_grado_director
from app.repositories.trabajo_grado_director_repo import TrabajoGradoDirectorRepository

router = APIRouter(prefix="/trabajoGradoDirector", tags=["Gestión de los trabajos de grados asignados a los profesores"])
repo = TrabajoGradoDirectorRepository()

@router.get("/")
def obtener_trabajos_de_grado_por_director():
    return repo.obtenerTrabajosDeGradoPorDirector()


@router.get("/{id_trabajo_grado_director}")
def obtener_trabajo_grado_por_director_por_id(id_trabajo_grado_director: int):
    Trabajo_grado_director = repo.obtenerTrabajoDeGradoDirectorPorId(id_trabajo_grado_director)
    
    if not Trabajo_grado_director:
        raise HTTPException(status_code= 404, detail="trabajo de grado por director no encontrado")
    return Trabajo_grado_director


@router.post("/")
def crear_trabajo_grado_por_director(trabajo_grado_director: Crear_trabajo_grado_director):
    nuevo_trabajo_grado_por_director = repo.crearRelacionTrabajoGradoPorDirector(trabajo_grado_director)
    return {"Mensaje ": "Trabajo de grado asignado exitosamente", "id: ": nuevo_trabajo_grado_por_director}



@router.put("/{id_trabajo_grado_director}")
def actualizar_trabajo_grado_por_director(id_trabajo_grado_director: int, trabajo_grado_director: Actualizar_trabajo_grado_director):
    actualizar_trabajo_grado_director = repo.actualizarTrabajoGradoPorDirector(id_trabajo_grado_director, trabajo_grado_director)
    
    return {
        "Mensaje": "Asignación del trabajo actualizado exitosamente",
        "Actualizado": actualizar_trabajo_grado_director
    }
    


@router.delete("/{id_trabajo_grado_director}")
def eliminar_trabajo_grado_por_director(id_trabajo_grado_director: int): 
    eliminar_trabajo_por_director = repo.eliminarTrabajoDeGradoPorDirector(id_trabajo_grado_director)
    if not eliminar_trabajo_por_director:
        raise HTTPException(status_code= 404, detail= "trabajo de grado por profesor no fue encontrado")
    return {"Mensaje": "Trabajo de grado por profesor eliminado correctamente"}

