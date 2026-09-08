from pydantic import BaseModel
from typing import Optional


class Modulo_rol(BaseModel):

    id_modulo_rol: Optional[int] = None

    id_rol: int

    id_modulo: int

    puede_leer: Optional[bool] = True

    puede_crear: Optional[bool] = False

    puede_editar: Optional[bool] = False

    puede_eliminar: Optional[bool] = False

    estado: Optional[bool] = True