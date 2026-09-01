from pydantic import BaseModel
from typing import Optional


class Modulo_rol(BaseModel):
    id_modulo_rol: Optional[int] = None
    id_rol: Optional[int] = None
    id_modulo: Optional[int] = None
    id_permiso: Optional[int] = None