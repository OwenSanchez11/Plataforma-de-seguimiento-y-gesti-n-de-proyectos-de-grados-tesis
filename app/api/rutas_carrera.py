from fastapi import APIRouter
from app.models.carrera import CarreraCrear, ActualizarCarrera
from app.repositories.carrera_repo import CarreraRepository


router = APIRouter(
    prefix="/carreras",
    tags=["Gestión de carreras"]
)

repo = CarreraRepository()


@router.get("/")
def obtener_carreras():
    return repo.obtenerCarreras()


@router.get("/{id_carrera}")
def obtener_carrera_por_id(id_carrera: int):
    return repo.obtenerCarreraPorId(id_carrera)


@router.post("/")
def crear_carrera(carrera: CarreraCrear):
    return repo.crearCarrera(carrera)


@router.put("/{id_carrera}")
def actualizar_carrera(
    id_carrera: int,
    carrera: ActualizarCarrera
):
    return repo.actualizarCarrera(id_carrera, carrera)


@router.delete("/{id_carrera}")
def eliminar_carrera(id_carrera: int):
    return repo.eliminarCarrera(id_carrera)