from pydantic import BaseModel
from typing import Optional
from datetime import date


class EquipoTrabajoCrear(BaseModel):
    id_trabajo_grado: int
    id_usuario: int
    id_rol_proyecto: int
    observaciones: Optional[str] = None
    fecha_asignacion: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    estado: bool = True


class ActualizarEquipoTrabajo(BaseModel):
    id_trabajo_grado: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol_proyecto: Optional[int] = None
    observaciones: Optional[str] = None
    fecha_asignacion: Optional[date] = None
    fecha_finalizacion: Optional[date] = None
    estado: Optional[bool] = None