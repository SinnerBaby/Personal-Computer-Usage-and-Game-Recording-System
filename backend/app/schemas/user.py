"""
用户相关数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserLogin(BaseModel):
    """用户登录"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """更新用户"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, description="头像路径")


class ChangePassword(BaseModel):
    """修改密码"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=50, description="新密码")


class UserResponse(UserBase):
    """用户响应"""
    id: int
    avatar: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token 响应"""
    token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    user: UserResponse


class TokenRefresh(BaseModel):
    """刷新 Token"""
    refresh_token: str = Field(..., description="刷新令牌")
