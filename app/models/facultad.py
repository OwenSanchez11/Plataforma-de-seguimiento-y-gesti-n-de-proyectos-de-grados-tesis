from pydantic import BaseModel


class FacultadCrear(BaseModel):
    nombre_facultad: str
    codigo_facultad: str | None = None


class ActualizarFacultad(BaseModel):
    nombre_facultad: str | None = None
    codigo_facultad: str | None = None