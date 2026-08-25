from pydantic import BaseModel
from typing import Optional


class Trabajo_grado_jurado(BaseModel): 
    id_trabajo_grado_jurado: Optional[int] = None
    id_trabajo_grado: int
    id_profesor: int
    
class Crear_trabajo_grado_jurado(BaseModel):
    id_trabajo_grado: int
    id_profesor: int

class Actualizar_trabajo_grado_jurado(BaseModel):
    id_trabajo_grado: int
    id_profesor: int