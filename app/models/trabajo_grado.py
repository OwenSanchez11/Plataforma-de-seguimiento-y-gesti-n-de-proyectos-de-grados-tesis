from pydantic import BaseModel
from typing import Optional
import datetime

class Trabajo_grado(BaseModel):
    id_trabajo_grado: Optional[int] = None
    titulo: str 
    descripcion: str
    estado: str
    fecha_inicio: datetime.date
    fecha_estimada_finalizacion: datetime.date
    
class CrearTrabajoGrado(BaseModel):
    titulo: str 
    descripcion: str
    estado: str
    fecha_inicio: datetime.date
    fecha_estimada_finalizacion: datetime.date
    
class ActualizarTrabajoGrado(BaseModel): 
    titulo: str
    estado: str
    fecha_estimada_finalizacion: datetime.date  
    
