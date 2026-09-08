from pydantic import BaseModel
from typing import Optional
from datetime import date


class Evaluacion(BaseModel):

    id_evaluacion: Optional[int] = None

    id_trabajo_grado: int

    id_usuario: int

    nota: Optional[float] = None

    veredicto: Optional[str] = None

    observaciones: Optional[str] = None

    fecha_evaluacion: Optional[date] = None

    estado: Optional[bool] = True