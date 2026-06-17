import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import LoginIn, LoginOut, RefreshTokenIn, RefreshTokenOut
from auth_utils import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from datetime import timedelta, datetime
from database import get_db
from sqlalchemy.orm import Session
from models import RefreshToken

router = APIRouter(prefix="/api/auth", tags=["Auth"])

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

_bearer = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    """JWT access tokenni tekshirish va validatsiya qilish"""
    try:
        token = credentials.credentials
        payload = decode_access_token(token)

        # Token ichidagi username ni tekshirish
        username = payload.get("sub")
        if username is None:
            raise HTTPException(401, "Token noto'g'ri formatda")

        return payload
    except ValueError as e:
        raise HTTPException(401, str(e))
    except Exception:
        raise HTTPException(401, "Token noto'g'ri yoki muddati o'tgan")


@router.post("/login", response_model=LoginOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    """
    Login endpoint - username va parol tekshiradi va access + refresh tokenlarni qaytaradi
    - Access token: 30 daqiqa (qisqa muddatli)
    - Refresh token: 7 kun (uzoq muddatli)
    """
    if data.username == ADMIN_USERNAME and data.password == ADMIN_PASSWORD:
        # Access token yaratish (30 daqiqa)
        access_token = create_access_token(
            data={"sub": data.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        # Refresh token yaratish (7 kun)
        refresh_token = create_refresh_token(data={"sub": data.username})

        # Refresh tokenni database ga saqlash
        refresh_payload = decode_refresh_token(refresh_token)
        jti = refresh_payload.get("jti")
        expires_at = datetime.utcfromtimestamp(refresh_payload.get("exp"))

        db_token = RefreshToken(
            jti=jti,
            username=data.username,
            expires_at=expires_at,
            revoked=0
        )
        db.add(db_token)
        db.commit()

        return LoginOut(
            access=True,
            access_token=access_token,
            refresh_token=refresh_token
        )

    raise HTTPException(401, "Login yoki parol noto'g'ri")


@router.post("/refresh", response_model=RefreshTokenOut)
def refresh(data: RefreshTokenIn, db: Session = Depends(get_db)):
    """
    Refresh token endpoint - refresh token bilan yangi access token olish
    """
    try:
        # Refresh tokenni decode qilish
        payload = decode_refresh_token(data.refresh_token)
        jti = payload.get("jti")
        username = payload.get("sub")

        # Database dan refresh tokenni topish
        db_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

        if not db_token:
            raise HTTPException(401, "Refresh token topilmadi")

        if db_token.revoked == 1:
            raise HTTPException(401, "Refresh token bekor qilingan")

        if db_token.expires_at < datetime.utcnow():
            raise HTTPException(401, "Refresh token muddati tugagan")

        # Yangi access token yaratish
        new_access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return RefreshTokenOut(access_token=new_access_token)

    except ValueError as e:
        raise HTTPException(401, str(e))
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(401, "Refresh token noto'g'ri")


@router.post("/logout")
def logout(
    data: RefreshTokenIn,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(_bearer)
):
    """
    Logout endpoint - refresh tokenni bekor qilish
    """
    try:
        # Refresh tokenni decode qilish
        payload = decode_refresh_token(data.refresh_token)
        jti = payload.get("jti")

        # Database dan tokenni topish va bekor qilish
        db_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()

        if db_token:
            db_token.revoked = 1
            db.commit()

        return {"message": "Muvaffaqiyatli chiqildi"}

    except Exception:
        # Logout da xatolik bo'lsa ham, user uchun success qaytarish
        return {"message": "Muvaffaqiyatli chiqildi"}
