"""
仪表盘 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date

from app.database import get_db
from app.models.user import User
from app.models.app_usage import AppUsage
from app.models.game import Game, GameSession
from app.utils.dependencies import get_current_user
from app.utils.response import success

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取仪表盘概览数据"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # 今日数据
    today_stats = db.query(
        func.sum(AppUsage.duration).label("total_duration"),
        func.count(AppUsage.id).label("record_count"),
    ).filter(AppUsage.date == today).first()
    
    # 昨日数据
    yesterday_stats = db.query(
        func.sum(AppUsage.duration).label("total_duration"),
    ).filter(AppUsage.date == yesterday).first()
    
    # 今日游戏时长
    today_game_duration = db.query(
        func.sum(GameSession.duration),
    ).filter(GameSession.date == today).scalar() or 0
    
    # 应用数量
    app_count = db.query(func.count(func.distinct(AppUsage.app_name))).scalar() or 0
    
    # 游戏数量
    game_count = db.query(func.count(Game.id)).scalar() or 0
    
    # 最常用应用
    most_used_app = db.query(
        AppUsage.app_name,
        func.sum(AppUsage.duration).label("duration"),
    ).filter(AppUsage.date == today).group_by(AppUsage.app_name).order_by(
        func.sum(AppUsage.duration).desc()
    ).first()
    
    # 计算变化
    today_total = today_stats.total_duration if today_stats and today_stats.total_duration else 0
    yesterday_total = yesterday_stats.total_duration if yesterday_stats and yesterday_stats.total_duration else 0
    
    total_change = today_total - yesterday_total
    total_change_pct = (total_change / yesterday_total * 100) if yesterday_total > 0 else 0
    
    return success(
        data={
            "total_duration": today_total,
            "active_duration": today_total,  # 简化处理
            "idle_duration": 0,
            "game_duration": today_game_duration,
            "app_count": app_count,
            "game_count": game_count,
            "vs_yesterday": {
                "total_change": total_change,
                "total_change_pct": round(total_change_pct, 1),
                "game_change": 0,
                "game_change_pct": 0,
            },
            "most_used_app": {
                "name": most_used_app.app_name,
                "duration": most_used_app.duration,
            } if most_used_app else None,
            "most_played_game": None,
        }
    )


@router.get("/trend")
async def get_trend_data(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取趋势数据"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    
    # 查询每日数据
    daily_data = db.query(
        AppUsage.date,
        func.sum(AppUsage.duration).label("total_duration"),
    ).filter(
        AppUsage.date >= start_date,
        AppUsage.date <= end_date,
    ).group_by(AppUsage.date).all()
    
    # 构建日期列表
    labels = []
    total_durations = []
    current_date = start_date
    data_dict = {str(d.date): d.total_duration for d in daily_data}
    
    while current_date <= end_date:
        date_str = str(current_date)
        labels.append(date_str)
        total_durations.append(data_dict.get(date_str, 0))
        current_date += timedelta(days=1)
    
    # 计算汇总
    avg_daily = sum(total_durations) / len(total_durations) if total_durations else 0
    max_duration = max(total_durations) if total_durations else 0
    max_day = labels[total_durations.index(max_duration)] if total_durations else ""
    
    return success(
        data={
            "labels": labels,
            "series": {
                "total_duration": total_durations,
                "active_duration": total_durations,
                "game_duration": [0] * len(labels),
            },
            "summary": {
                "avg_daily_total": int(avg_daily),
                "avg_daily_game": 0,
                "max_day": max_day,
                "max_duration": max_duration,
            },
        }
    )
