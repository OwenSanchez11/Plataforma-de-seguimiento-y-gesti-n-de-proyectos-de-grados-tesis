from pydantic import BaseModel
from typing import Optional
from datetime import date

class Retroalimentacion(BaseModel):
    id_retroalimentacion: Optional[int] = None
    id_entrega: Optional[int] = None
    id_usuario: Optional[int] = None
    comentario: Optional[str] = None
    estado: Optional[str] = None
    fecha_creacion: Optional[date] = None
    
