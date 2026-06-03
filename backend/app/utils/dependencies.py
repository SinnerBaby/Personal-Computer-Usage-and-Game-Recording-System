"""
依赖注入函数
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> User:
    """获取当前认证用户"""
    # ===== 开发阶段：跳过 token 验证，直接返回 admin =====
    # 无论 token 是否存在，直接返回 admin 用户
    user = db.query(User).filter(User.username == "admin").first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Admin user not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # ===== 上线后替换为下方的正式逻辑 =====
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )
    
    return user
    """
