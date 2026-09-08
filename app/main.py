from fastapi import FastAPI

from app.api import rutas_usuario
from app.api import rutas_rol
from app.api import rutas_rol_usuario
from app.api import rutas_trabajo_grado
from app.api import rutas_entrega
from app.api import rutas_avances
from app.api import rutas_retroalimentaciones
from app.api import rutas_facultad
from app.api import rutas_carrera
from app.api import rutas_equipo_trabajo
from app.api import rutas_evaluacion
from app.api import rutas_permiso
from app.api import rutas_modulo
from app.api import rutas_modulo_rol


app = FastAPI(
    title="Backend sistema de seguimiento de trabajos de grados",
    description="Sistema diseñado para hacer seguimiento a los trabajos de grado realizados por los estudiantes de la universidad",
    version="1.0.0"
)


app.include_router(rutas_usuario.router)
app.include_router(rutas_rol.router)
app.include_router(rutas_rol_usuario.router)
app.include_router(rutas_trabajo_grado.router)
app.include_router(rutas_entrega.router)
app.include_router(rutas_avances.router)
app.include_router(rutas_retroalimentaciones.router)
app.include_router(rutas_facultad.router)
app.include_router(rutas_carrera.router)
app.include_router(rutas_equipo_trabajo.router)
app.include_router(rutas_evaluacion.router)
app.include_router(rutas_permiso.router)
app.include_router(rutas_modulo.router)
app.include_router(rutas_modulo_rol.router)