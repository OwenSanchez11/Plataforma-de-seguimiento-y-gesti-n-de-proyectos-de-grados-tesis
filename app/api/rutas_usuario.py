from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Gestión de usuarios"])
repo = UsuarioRepository()


@router.get("/")
def obtener_usuarios():
    return repo.obtenerUsuarios()

@router.get("/{id_user}")
def obtener_usuarios_por_id(id_user: int):
    usuario = repo.obtenerPorId(id_user)
    if not usuario:
        raise HTTPException(status_code= 404, detail= "Usuario no encontrado")
    return usuario

@router.post("/")
def crear_usuario(usuario: Usuario):
    nuevo_id = repo.crearUsuario(usuario)
    return {"Mensaje ": "Usuario registrado exitosamente", "id": nuevo_id}


@router.put("/{id_user}")
def actualizar_usuario(id_user: int, usuario: Usuario):
    actualizado = repo.actualizarUsuario(id_user, usuario)

    return {
        "Mensaje": "Usuario actualizado exitosamente",
        "actualizado": actualizado
    }

@router.delete("/{id_user}")
def eliminar_usuario(id_user: int):
    exito = repo.eliminarUsuario(id_user)
    if not exito:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"Mensaje": "Usuario eliminado correctamente"}    
    