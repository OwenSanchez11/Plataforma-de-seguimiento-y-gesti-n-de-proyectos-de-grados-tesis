from pydantic import BaseModel
from typing import Optional
from datetime import date


class Hito(BaseModel):
    id_hito: Optional[int] = None
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str


class CrearHito(BaseModel):
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str


class ActualizarHito(BaseModel):
    id_trabajo_grado: int
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_limite: date
    estado: str