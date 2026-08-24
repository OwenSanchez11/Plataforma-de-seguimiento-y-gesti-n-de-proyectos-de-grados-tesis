from pydantic import BaseModel
from typing import Optional

class RolUsuario(BaseModel):
    id_rol_usuario: Optional[int] = None
    id_usuario: int
    id_rol: int
    
class CrearRelacionUsuarioRol(BaseModel):
    id_usuario: int
    id_rol: int
    
class RolUsuarioRespuesta(BaseModel):
    id_usuario: int
    id_rol: int
    
class ActualizarRelacionRolYUsuario(BaseModel):
    id_rol: int