"""
安全工具函数
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_access_token(user_id: int, username: str) -> str:
    """创建访问令牌"""
    return create_token(
        data={"sub": str(user_id), "username": username, "type": "access"},
        expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: int, username: str) -> str:
    """创建刷新令牌"""
    return create_token(
        data={"sub": str(user_id), "username": username, "type": "refresh"},
        expires_delta=timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
    )


def verify_token(token: str) -> Optional[dict]:
    """验证 Token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
