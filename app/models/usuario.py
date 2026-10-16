from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_user: Optional[int] = None
    id_carrera: int
    id_rol: int
    username: str
    nombre: str
    apellido: str
    email: str
    documento: str
    contrasena: str
    estado: bool = True
