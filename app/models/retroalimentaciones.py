from pydantic import BaseModel
from typing import Optional


class Retroalimentacion(BaseModel):
    id_retroalimentacion: Optional[int] = None
    id_avance: int
    id_usuario: int
    comentario: str
    estado: Optional[bool] = True