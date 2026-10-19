import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
load_dotenv()

admin = 1
coordinador = 2
docente = 4
estudiante = 5
 
bearer = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRA_MINUTOS = 60

def hashear_password(contrasena: str) -> str:
    sal = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(contrasena.encode("utf-8"), sal)
    return hash_bytes.decode("utf-8")

def verificar_password(contrasena: str, contrasena_hash: str) -> bool:
    return bcrypt.checkpw(
        contrasena.encode("utf-8"),
        contrasena_hash.encode("utf-8")
    )
    
    
def crearToken(datos: dict) -> str: 
    payload = {
        **datos,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_MINUTOS)
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        return jwt.decode(
            credenciales.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="La sesión expiró")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def solo_roles(*roles_permitidos):
    def verificar(usuario = Depends(usuario_actual)):
        if usuario["id_rol"] not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tienes permiso")
        return usuario
    return verificar