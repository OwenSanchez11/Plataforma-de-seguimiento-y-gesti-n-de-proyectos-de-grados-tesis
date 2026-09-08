from pydantic import BaseModel
from typing import Optional


class ModuloRol(BaseModel):
    id_rol: int
    id_modulo: int
    puede_leer: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
    estado: bool = True


class ActualizarModuloRol(BaseModel):
    id_rol: Optional[int] = None
    id_modulo: Optional[int] = None
    puede_leer: Optional[bool] = None
    puede_crear: Optional[bool] = None
    puede_editar: Optional[bool] = None
    puede_eliminar: Optional[bool] = None
    estado: Optional[bool] = None