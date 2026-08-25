from fastapi import FastAPI
from app.api import rutas_usuario
from app.api import rutas_rol
from app.api import rutas_rol_usuario
from app.api import rutas_trabajo_grado
from app.api import rutas_trabajo_grado_estudiantes
from app.api import rutas_trabajo_grado_director
from app.api import rutas_trabajo_grado_jurado
from app.api import rutas_entrega
from app.api import rutas_hito
from app.api import rutas_retroalimentaciones


app = FastAPI(title="Backend sistema de seguimiento de trabajos de grados",
              description="Sistema diseñado para hacer seguimiento a los trabajos de grados realizadaos por los estudiantes de la universidad", version="1.0.0")

app.include_router(rutas_usuario.router)
app.include_router(rutas_rol.router)
app.include_router(rutas_rol_usuario.router)
app.include_router(rutas_trabajo_grado.router)
app.include_router(rutas_trabajo_grado_estudiantes.router)
app.include_router(rutas_trabajo_grado_director.router)
app.include_router(rutas_trabajo_grado_jurado.router)
app.include_router(rutas_entrega.router)
app.include_router(rutas_hito.router)
app.include_router(rutas_retroalimentaciones.router)
