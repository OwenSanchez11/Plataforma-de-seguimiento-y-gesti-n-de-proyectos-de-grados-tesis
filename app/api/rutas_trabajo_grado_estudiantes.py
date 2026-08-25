from fastapi import APIRouter, HTTPException
from app.models.trabajo_grado_estudiante import Trabajo_grado_estudiante
from app.models.trabajo_grado_estudiante import CrearTrabajoGradoPorEstudiante
from app.models.trabajo_grado_estudiante import ActualizarTrabajoGradoPorEstudiante
from app.repositories.trabajo_grado_estudiante_repo import TrabajoGradoEstudianteRepository

router = APIRouter(prefix="/trabajo_grado_estudiantes", tags=["Gestión de los trabajos de grados asignados a los estudiantes"])
repo = TrabajoGradoEstudianteRepository()

@router.get("/")
def obtener_trabajos_de_grado_por_estudiante():
    return repo.obtenerTrabajosPorEstudiante()

@router.get("/{id_trabajo_grado_estudiante}")
def obtener_trabajo_grado_por_estudiante_por_id(id_trabajo_grado_estudiante: int):
    Trabajo_grado_estudiante = repo.obtenerTrabajoGradoPorEstudiantePorId(id_trabajo_grado_estudiante)
    
    if not Trabajo_grado_estudiante:
        raise HTTPException(status_code= 404, detail="trabajo de grado por estudiante no encontrado")
    return Trabajo_grado_estudiante


@router.post("/")
def crear_trabajo_grado_por_estudiante(trabajo_grado_estudiante: CrearTrabajoGradoPorEstudiante):
    nuevo_trabajo_grado_por_estudiante = repo.crearRelacionTrabajoGradoPorEstudiante(trabajo_grado_estudiante)
    return {"Mensaje ": "Trabajo de grado asignado exitosamente", "id: ": nuevo_trabajo_grado_por_estudiante}



@router.put("/{id_trabajo_grado_estudiante}")
def actualizar_trabajo_grado_por_estudiante(id_trabajo_grado_estudiante: int, trabajo_grado_estudiante: ActualizarTrabajoGradoPorEstudiante):
    actualizar_trabajo_grado_estudiante = repo.actualizarTrabajoGradoPorEstudiante(id_trabajo_grado_estudiante, trabajo_grado_estudiante)
    
    return {
        "Mensaje": "Asignación del trabajo actualizado exitosamente",
        "Actualizado": actualizar_trabajo_grado_estudiante
    }
    


@router.delete("/{id_trabajo_grado_estudiante}")
def eliminar_trabajo_grado_por_estudiante(id_trabajo_grado_estudiante: int): 
    eliminar_trabajo_por_estudiante = repo.eliminarTrabajoGradoPorEstudiante(id_trabajo_grado_estudiante)
    if not eliminar_trabajo_por_estudiante:
        raise HTTPException(status_code= 404, detail= "trabajo de grado por estudiante no fue encontrado")
    return {"Mensaje": "Trabajo de grado por estudiante eliminado correctamente"}

