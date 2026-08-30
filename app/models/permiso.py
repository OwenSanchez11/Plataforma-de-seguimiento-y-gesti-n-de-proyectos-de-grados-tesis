from pydantic import BaseModel
from typing import Optional


class Permiso(BaseModel):

    id_permiso: Optional[int] = None

    nombre_permiso: Optional[str] = None