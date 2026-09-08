from pydantic import BaseModel
from typing import Optional


class Rol_proyecto(BaseModel):
    id_rol_proyecto: Optional[int] = None
    nombre: Optional[str] = None
    estado: Optional[bool] = None