import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import LoginIn, LoginOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_TOKEN   = os.getenv("SECRET_TOKEN", "eduplan-secret-2024")

_bearer = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(401, "Token noto'g'ri yoki muddati o'tgan")


@router.post("/login", response_model=LoginOut)
def login(data: LoginIn):
    if data.username == ADMIN_USERNAME and data.password == ADMIN_PASSWORD:
        return LoginOut(access=True, token=SECRET_TOKEN)
    raise HTTPException(401, "Login yoki parol noto'g'ri")
