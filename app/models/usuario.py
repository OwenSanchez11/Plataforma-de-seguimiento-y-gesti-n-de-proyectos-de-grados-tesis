from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_user: Optional[int] = None
    id_carrera: Optional[int] = None
    id_rol: Optional[int] = None
    username: str
    nombre: str
    apellido: str
    email: str
    documento: str
    contrasena: str
    estado: Optional[bool] = True