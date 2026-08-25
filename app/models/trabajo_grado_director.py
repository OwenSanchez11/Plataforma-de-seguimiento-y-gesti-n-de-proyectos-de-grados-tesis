from pydantic import BaseModel
from typing import Optional

class Trabajo_grado_director(BaseModel): 
    id_trabajo_grado_director: Optional[int] = None
    id_trabajo_grado: int
    id_profesor: int
    tipo_director: str
    
class Crear_trabajo_grado_director(BaseModel): 
    id_trabajo_grado: int
    id_profesor: int
    tipo_director: str
    
class Actualizar_trabajo_grado_director(BaseModel):
    id_trabajo_grado: int
    id_profesor: int
    tipo_director: str
     