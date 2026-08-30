from pydantic import BaseModel
from typing import Optional


class Carrera(BaseModel):

    id_carrera: Optional[int] = None

    id_facultad: Optional[int] = None

    nombre_carrera: Optional[str] = None

    codigo_carrera: Optional[str] = None