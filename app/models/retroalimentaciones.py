from pydantic import BaseModel
from typing import Optional
from datetime import date

class Retroalimentacion(BaseModel):
    id_retroalimentacion: Optional[int] = None
    id_entrega: int
    id_profesor: int
    comentario: str
    estado: str
    fecha_creacion: date
    
class CrearRetroalimentacion(BaseModel):
    id_entrega: int
    id_profesor: int
    comentario: str
    estado: str
    fecha_creacion: date
    
class ActualizarRetroalimentacion(BaseModel):
    comentario: str
    estado: str
    fecha_creacion: date