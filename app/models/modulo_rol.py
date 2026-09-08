from pydantic import BaseModel
from typing import Optional


class ModuloRol(BaseModel):
    id_rol: Optional[int] = None
    id_modulo: Optional[int] = None
    puede_leer: Optional[bool] = None
    puede_crear: Optional[bool] = None
    puede_editar: Optional[bool] = None
    puede_eliminar: Optional[bool] = None
    estado: Optional[bool] = None

    
    
    