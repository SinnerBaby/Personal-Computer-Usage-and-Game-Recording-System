"""
配置管理
"""
import json
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库
    DATABASE_URL: str = "sqlite:///./data/tracker.db"
    
    # JWT 配置
    JWT_SECRET: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 小时
    JWT_REFRESH_EXPIRE_DAYS: int = 7  # 7 天
    
    # CORS 配置
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # 文件上传
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 备份
    BACKUP_DIR: str = "./backups"
    
    # 日志
    LOG_LEVEL: str = "INFO"
    
    # 采集配置
    IDLE_THRESHOLD: int = 300  # 闲置判定阈值（秒）
    SYNC_INTERVAL: int = 60  # 数据同步间隔（秒）
    DATA_RETENTION_DAYS: int = 365  # 数据保留天数
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()
