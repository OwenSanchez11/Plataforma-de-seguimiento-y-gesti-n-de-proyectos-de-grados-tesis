from pydantic import BaseModel
from typing import Optional
from datetime import date


class Asignacion(BaseModel):
    id_trabajo_grado: int
    id_usuario: int
    id_rol_proyecto: int
    observaciones: Optional[str] = None
    fecha_asignacion: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    estado: Optional[bool] = True