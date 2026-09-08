from pydantic import BaseModel
from typing import Optional


class Carrera(BaseModel):

    id_carrera: Optional[int] = None

    id_facultad: int

    nombre_carrera: str

    codigo_carrera: Optional[str] = None

    estado: Optional[bool] = True