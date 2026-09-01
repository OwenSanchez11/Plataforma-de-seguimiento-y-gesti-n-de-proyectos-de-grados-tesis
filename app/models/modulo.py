from pydantic import BaseModel
from typing import Optional

class Modulo(BaseModel):
    id_modulo: Optional[int] =  None
    nombre_modulo: Optional[str] = None
    estado: Optional[bool]
    
    