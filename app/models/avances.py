from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Avances(BaseModel):

    id_avance: Optional[int] = None

    id_trabajo_grado: int

    titulo: str

    subido_por: int

    descripcion: Optional[str] = None

    numero_version: Optional[int] = None

    nombre_archivo: Optional[str] = None

    ruta_archivo: Optional[str] = None

    tamano_bytes: Optional[int] = None

    fecha_inicio: Optional[datetime] = None

    fecha_entrega: Optional[datetime] = None

    fecha_limite: Optional[datetime] = None

    estado: Optional[bool] = True