from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_user: Optional[int] = None
    id_carrera: Optional[int] = None
    username: Optional[str] = None 
    nombre: Optional[str] = None 
    apellido: Optional[str] = None 
    email: Optional[str] = None 
    documento: Optional[str] = None 
    contraseña: Optional[str] = None
