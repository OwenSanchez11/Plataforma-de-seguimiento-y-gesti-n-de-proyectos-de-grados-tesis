from fastapi import HTTPException
from app.core.database import Database
from app.models.login import LoginRequest
from app.core.security import verificar_password  
from app.core.security import crearToken

class LoginRepository:
    def __init__(self):
        self.db = Database()

    def login(self, datos: LoginRequest):
        conn = self.db.getConnection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_user, nombre, apellido, email, id_rol, contrasena "
                "FROM usuario WHERE email = %s AND estado = true",
                (datos.email,)
            )
            usuario = cursor.fetchone()
        finally:
            conn.close()

        if usuario is None or not verificar_password(datos.contrasena, usuario["contrasena"]):
            raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

        usuario.pop("contrasena")  
        
        token = crearToken({
            "sub": str(usuario["id_user"]),
            "id_rol": usuario["id_rol"]
        })
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": usuario
        }