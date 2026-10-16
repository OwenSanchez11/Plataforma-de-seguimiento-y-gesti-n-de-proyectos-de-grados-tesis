from pydantic import BaseModel
from typing import Optional
from typing import Optional, Literal


class Rol(BaseModel):
    id_rol: Optional[int] = None
    rol_nombre: str
    estado: Optional[bool] = True
    ambito: Literal["SISTEMA", "PROYECTO"]