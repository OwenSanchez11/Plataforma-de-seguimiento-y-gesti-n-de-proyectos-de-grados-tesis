from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
from app.core.security import admin, coordinador, estudiante, docente, solo_roles, usuario_actual

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de usuarios"],
    dependencies=[Depends(usuario_actual)])


repo = UsuarioRepository()


@router.get("/", dependencies=[Depends(solo_roles(admin, docente, coordinador))])
def obtener_usuarios():
    return repo.obtenerUsuarios()


@router.get("/{id_user}", dependencies=[Depends(solo_roles(admin))])
def obtener_usuarios_por_id(id_user: int):

    usuario = repo.obtenerPorId(id_user)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/", dependencies=[Depends(solo_roles(admin, coordinador))])
def crear_usuario(usuario: Usuario):
    if not usuario.contrasena: 
        raise HTTPException(status_code=400, detail="La contraseña es obligatoria al crear un usuario")
    return repo.crearUsuario(usuario)


@router.put("/{id_user}", dependencies=[Depends(solo_roles(admin))])
def actualizar_usuario(id_user: int, usuario: Usuario):

    actualizado = repo.actualizarUsuario(
        id_user,
        usuario
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "Mensaje": "Usuario actualizado exitosamente"
    }


@router.delete("/{id_user}", dependencies=[Depends(solo_roles(admin))])
def eliminar_usuario(id_user: int):

    eliminado = repo.eliminarUsuario(id_user)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "Mensaje": "Usuario eliminado correctamente"
    }