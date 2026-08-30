from pydantic import BaseModel
from datetime import date


class AsignacionCrear(BaseModel):

    id_trabajo_grado: int

    id_usuario: int

    id_rol: int

    fecha_asignacion: date | None = None

    estado: bool | None = True


class ActualizarAsignacion(BaseModel):

    id_trabajo_grado: int | None = None

    id_usuario: int | None = None

    id_rol: int | None = None

    fecha_asignacion: date | None = None

    estado: bool | None = None