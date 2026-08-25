from pydantic import BaseModel
from typing import Optional
from datetime import date


class Entrega(BaseModel):
    id_entrega: Optional[int] = None
    id_hito: int
    numero_version: int
    nombre_archivo: str
    ruta_archivo: str
    comentarios: Optional[str] = None
    estado: str
    fecha_entrega: date


class CrearEntrega(BaseModel):
    id_hito: int
    numero_version: int
    nombre_archivo: str
    ruta_archivo: str
    comentarios: Optional[str] = None
    estado: str
    fecha_entrega: date


class ActualizarEntrega(BaseModel):
    id_hito: int
    numero_version: int
    nombre_archivo: str
    ruta_archivo: str
    comentarios: Optional[str] = None
    estado: str
    fecha_entrega: date