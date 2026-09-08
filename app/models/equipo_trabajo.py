from pydantic import BaseModel
from typing import Optional
from datetime import date


class EquipoTrabajo(BaseModel):
    id_equipo: Optional[int] = None
    id_trabajo_grado: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol_proyecto: Optional[int] = None
    observaciones: Optional[str] = None
    fecha_asignacion: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    estado: bool = True

