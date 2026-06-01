"""
认证相关 API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserCreate, TokenResponse, TokenRefresh, UserResponse, ChangePassword
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.utils.response import success
from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("/login", response_model=dict)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        return {"code": 40001, "message": "用户名或密码错误", "data": None, "timestamp": 0}
    
    # 验证密码
    if not verify_password(user_data.password, user.password_hash):
        return {"code": 40001, "message": "用户名或密码错误", "data": None, "timestamp": 0}
    
    # 生成 Token
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)
    
    return success(
        data={
            "token": access_token,
            "refreshToken": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
            },
        }
    )


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        return {"code": 40002, "message": "用户名已存在", "data": None, "timestamp": 0}
    
    # 创建用户
    user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        nickname=user_data.nickname or user_data.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成 Token
    access_token = create_access_token(user.id, user.username)
    refresh_token = create_refresh_token(user.id, user.username)
    
    return success(
        data={
            "token": access_token,
            "refreshToken": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "nickname": user.nickname,
            },
        }
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """刷新 Token"""
    payload = verify_token(token_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        return {"code": 40102, "message": "无效的刷新令牌", "data": None, "timestamp": 0}
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"code": 40102, "message": "用户不存在", "data": None, "timestamp": 0}
    
    # 生成新的访问令牌
    access_token = create_access_token(user.id, user.username)
    
    return success(data={"token": access_token})


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return success(
        data={
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
        }
    )


@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """修改密码"""
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        return {"code": 40001, "message": "旧密码错误", "data": None, "timestamp": 0}
    
    # 更新密码
    current_user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return success(message="密码修改成功")
