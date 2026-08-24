from pydantic import BaseModel
from typing import Optional

class Rol(BaseModel):
    id_rol: Optional[int] = None
    rol_nombre: str
    
class CrearRol(BaseModel):
    rol_nombre: str
    
class ActualizarRol(BaseModel):
    rol_nombre: str