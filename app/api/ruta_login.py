from fastapi import APIRouter
from app.models.login import LoginRequest
from app.repositories.login_repo import LoginRepository

router = APIRouter(
    prefix="/auth",
    tags=["Login de usuario"]
)

repo = LoginRepository()


@router.post("/login")
def login(datos: LoginRequest):
    return repo.login(datos)