from pydantic import BaseModel
from typing import Optional


class Trabajo_grado(BaseModel):
    id_trabajo_grado: Optional[int] = None
    titulo: str
    descripcion: str
    estado: str
    fecha_inicio: date
    fecha_estimada_finalizacion: date
    
class crearTrabajoGrado(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    fecha_inicio: date
    fecha_estimada_finalizacion: date
    
    
    