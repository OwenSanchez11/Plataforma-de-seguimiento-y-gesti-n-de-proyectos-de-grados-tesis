from pydantic import BaseModel


class CarreraCrear(BaseModel):
    id_facultad: int
    nombre_carrera: str
    codigo_carrera: str | None = None


class ActualizarCarrera(BaseModel):
    id_facultad: int | None = None
    nombre_carrera: str | None = None
    codigo_carrera: str | None = None