from pydantic import BaseModel
from typing import Optional
from datetime import date

class Trabajo_grado(BaseModel):
    id_trabajo_grado: Optional[int] = None
    id_carrera: Optional[int] = None
    titulo: Optional[str] = None 
    resumen: Optional[str] = None
    linea_investigacion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[str] = None
    fecha_sustentacion: Optional[date] = None
    observaciones_finales: Optional[str] = None

