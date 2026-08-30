from fastapi import APIRouter

from app.models.asignacion import AsignacionCrear, ActualizarAsignacion

from app.repositories.asignacion_repo import AsignacionRepository


router = APIRouter(

    prefix="/asignaciones",

    tags=["Gestión de asignaciones"]

)

repo = AsignacionRepository()


@router.get("/")
def obtener_asignaciones():

    return repo.obtenerAsignaciones()


@router.get("/{id_asignacion}")
def obtener_asignacion_por_id(id_asignacion: int):

    return repo.obtenerAsignacionPorId(id_asignacion)


@router.post("/")
def crear_asignacion(asignacion: AsignacionCrear):

    return repo.crearAsignacion(asignacion)


@router.put("/{id_asignacion}")
def actualizar_asignacion(

    id_asignacion: int,

    asignacion: ActualizarAsignacion

):

    return repo.actualizarAsignacion(id_asignacion, asignacion)


@router.delete("/{id_asignacion}")
def eliminar_asignacion(id_asignacion: int):

    return repo.eliminarAsignacion(id_asignacion)