from pydantic import BaseModel
from typing import Optional
from datetime import date


class Avances(BaseModel):

    id_avances: Optional[int] = None

    id_trabajo_grado: Optional[int] = None

    titulo: Optional[str] = None

    descripcion: Optional[str] = None

    fecha_inicio: Optional[date] = None

    fecha_limite: Optional[date] = None

    estado: Optional[str] = None