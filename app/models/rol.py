from pydantic import BaseModel
from typing import Optional

class Rol(BaseModel):
    id_rol: Optional[int] = None
    rol_nombre: Optional[str] = None
    