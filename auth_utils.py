"""
Authentication utilities for secure password hashing and JWT token generation
"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
import os
import secrets

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720  # 12 soat
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 kun (uzoq muddatli)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni hash bilan solishtirish"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Parolni hash qilish"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """JWT access token yaratish (qisqa muddatli - 30 daqiqa)"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """JWT refresh token yaratish (uzoq muddatli - 7 kun)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Har bir refresh token uchun unique identifier
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": secrets.token_urlsafe(32)  # JWT ID - har bir token uchun unique
    })

    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """JWT access tokenni decode qilish"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Token tipini tekshirish
        if payload.get("type") != "access":
            raise ValueError("Noto'g'ri token tipi")

        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token muddati tugagan")
    except jwt.InvalidTokenError:
        raise ValueError("Noto'g'ri token")


def decode_refresh_token(token: str) -> dict:
    """JWT refresh tokenni decode qilish"""
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])

        # Token tipini tekshirish
        if payload.get("type") != "refresh":
            raise ValueError("Noto'g'ri token tipi")

        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh token muddati tugagan")
    except jwt.InvalidTokenError:
        raise ValueError("Noto'g'ri refresh token")