from pydantic import BaseModel
from typing import Optional
from datetime import date


class Entrega(BaseModel):

    id_entrega: Optional[int] = None

    id_avances: Optional[int] = None

    numero_version: Optional[int] = None

    nombre_archivo: Optional[str] = None

    ruta_archivo: Optional[str] = None

    comentarios: Optional[str] = None

    estado: Optional[str] = None

    fecha_entrega: Optional[date] = None