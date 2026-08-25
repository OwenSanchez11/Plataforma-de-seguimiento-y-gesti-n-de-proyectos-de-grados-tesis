from pydantic import BaseModel
from typing import Optional

class Trabajo_grado_estudiante(BaseModel):
    id_trabajo_grado_estudiante: Optional[int] = None
    id_trabajo_grado: int
    id_estudiante: int
    
class CrearTrabajoGradoPorEstudiante(BaseModel): 
    id_trabajo_grado: int
    id_estudiante: int
    
class ActualizarTrabajoGradoPorEstudiante(BaseModel):
    id_trabajo_grado: int
    id_estudiante: int
    