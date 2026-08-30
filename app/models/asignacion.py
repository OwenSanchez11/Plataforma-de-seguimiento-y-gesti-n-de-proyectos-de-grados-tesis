from pydantic import BaseModel
from typing import Optional
from datetime import date


class Asignacion(BaseModel):

    id_asignacion: Optional[int] = None

    id_trabajo_grado: Optional[int] = None

    id_usuario: Optional[int] = None

    id_rol: Optional[int] = None

    fecha_asignacion: Optional[date] = None

    estado: Optional[bool] = None