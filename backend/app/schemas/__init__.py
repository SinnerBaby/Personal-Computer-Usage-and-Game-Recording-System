"""
Pydantic 数据模式包
"""
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.app_usage import (
    AppUsageResponse,
    AppUsageCreate,
    AppCategoryResponse,
    AppCategoryCreate,
)
from app.schemas.game import (
    GameResponse,
    GameCreate,
    GameUpdate,
    GameTagResponse,
    GameTagCreate,
    GameSessionResponse,
    GameSessionCreate,
)
from app.schemas.common import ApiResponse, PaginatedResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "AppUsageResponse",
    "AppUsageCreate",
    "AppCategoryResponse",
    "AppCategoryCreate",
    "GameResponse",
    "GameCreate",
    "GameUpdate",
    "GameTagResponse",
    "GameTagCreate",
    "GameSessionResponse",
    "GameSessionCreate",
    "ApiResponse",
    "PaginatedResponse",
]
