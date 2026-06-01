"""
系统设置 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_user
from app.utils.response import success
from app.config import settings

router = APIRouter()


@router.get("")
async def get_settings(
    current_user: User = Depends(get_current_user),
):
    """获取系统设置"""
    return success(
        data={
            "idle_threshold": settings.IDLE_THRESHOLD,
            "sync_interval": settings.SYNC_INTERVAL,
            "data_retention_days": settings.DATA_RETENTION_DAYS,
            "auto_cleanup": False,
        }
    )


@router.put("")
async def update_settings(
    settings_data: dict,
    current_user: User = Depends(get_current_user),
):
    """更新系统设置"""
    # 注意：这里简化处理，实际应该持久化到数据库或配置文件
    # 这里只是返回成功，实际项目中需要实现设置的持久化
    return success(
        data={
            "idle_threshold": settings_data.get("idle_threshold", settings.IDLE_THRESHOLD),
            "sync_interval": settings_data.get("sync_interval", settings.SYNC_INTERVAL),
            "data_retention_days": settings_data.get("data_retention_days", settings.DATA_RETENTION_DAYS),
            "auto_cleanup": settings_data.get("auto_cleanup", False),
        }
    )
