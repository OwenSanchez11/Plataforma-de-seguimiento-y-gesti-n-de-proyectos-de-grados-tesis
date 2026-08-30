from pydantic import BaseModel
from typing import Optional
from datetime import date


class Avances(BaseModel):
    id_avances: Optional[int] = None
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str


class CrearAvances(BaseModel):
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str


class ActualizarAvances(BaseModel):
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str