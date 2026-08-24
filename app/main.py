from fastapi import FastAPI
from app.api import rutas_usuario
from app.api import rutas_rol
from app.api import rutas_rol_usuario

app = FastAPI(title="Backend sistema de seguimiento de trabajos de grados",
              description="Sistema diseñado para hacer seguimiento a los trabajos de grados realizadaos por los estudiantes de la universidad", version="1.0.0")

app.include_router(rutas_usuario.router)
app.include_router(rutas_rol.router)
app.include_router(rutas_rol_usuario.router)
app.include_router(rutas_rol_trabajo_Grado.router)

@app.get("/")
def estadoDeMiApi(): 
    return{"Mensaje": "La API del CRUD se encuentra en linea y funcional"}