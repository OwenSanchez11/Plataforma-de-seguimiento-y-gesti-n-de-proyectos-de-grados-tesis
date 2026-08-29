from pydantic import BaseModel
from typing import Optional

class RolUsuario(BaseModel):
    id_rol_usuario: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol: Optional[int] = None
    
