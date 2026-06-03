"""
PC Usage Tracker API - 主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api.v1 import auth, dashboard, apps, games, stats, settings as settings_router, sync, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 迁移：添加缺少的字段
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            # 检查 exe_path 字段是否存在
            result = conn.execute(text("PRAGMA table_info(games)"))
            cols = [row[1] for row in result]
            if "exe_path" not in cols:
                conn.execute(text("ALTER TABLE games ADD COLUMN exe_path VARCHAR(500)"))
                conn.commit()
                print("数据库迁移: 添加 exe_path 字段")
    except Exception as e:
        print(f"数据库迁移跳过: {e}")
    
    # 创建数据库表（不覆盖已有表）
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成")
    yield
    # 关闭时清理
    print("应用关闭")


app = FastAPI(
    title="PC Usage Tracker API",
    version="1.0.0",
    description="个人电脑使用与游戏记录系统 API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["仪表盘"])
app.include_router(apps.router, prefix="/api/v1/apps", tags=["应用记录"])
app.include_router(games.router, prefix="/api/v1/games", tags=["游戏记录"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["统计分析"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["系统设置"])
app.include_router(sync.router, prefix="/api/v1/sync", tags=["数据同步"])
app.include_router(data.router, prefix="/api/v1/data", tags=["数据管理"])


@app.get("/", tags=["健康检查"])
async def root():
    """健康检查接口"""
    return {"message": "PC Usage Tracker API", "version": "1.0.0"}


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
