"""
统计分析 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, timedelta
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.app_usage import AppUsage
from app.models.game import Game, GameSession
from app.utils.dependencies import get_current_user
from app.utils.response import success

router = APIRouter()


@router.get("/trend")
async def get_usage_trend(
    dimension: str = Query("day", description="维度：day/week/month/year"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取使用趋势数据"""
    if not end_date:
        end_date = date.today()
    if not start_date:
        if dimension == "day":
            start_date = end_date - timedelta(days=6)
        elif dimension == "week":
            start_date = end_date - timedelta(weeks=7)
        elif dimension == "month":
            start_date = end_date - timedelta(days=180)
        else:
            start_date = end_date - timedelta(days=365)
    
    # 查询数据
    query = db.query(
        AppUsage.date,
        func.sum(AppUsage.duration).label("total_duration"),
    ).filter(
        AppUsage.date >= start_date,
        AppUsage.date <= end_date,
    ).group_by(AppUsage.date)
    
    results = query.all()
    
    # 构建数据
    data_dict = {str(r.date): r.total_duration for r in results}
    labels = []
    values = []
    
    current = start_date
    while current <= end_date:
        labels.append(str(current))
        values.append(data_dict.get(str(current), 0))
        current += timedelta(days=1)
    
    return success(
        data={
            "labels": labels,
            "values": values,
            "dimension": dimension,
        }
    )


@router.get("/time-distribution")
async def get_time_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取时段分布数据"""
    # 按小时统计
    hourly = db.query(
        extract("hour", AppUsage.start_time).label("hour"),
        func.sum(AppUsage.duration).label("duration"),
    ).group_by("hour").all()
    
    hourly_data = [0] * 24
    for h in hourly:
        hourly_data[int(h.hour)] = h.duration
    
    # 按星期统计
    weekly = db.query(
        extract("dow", AppUsage.start_time).label("dow"),
        func.sum(AppUsage.duration).label("duration"),
    ).group_by("dow").all()
    
    weekly_data = [0] * 7
    for w in weekly:
        weekly_data[int(w.dow)] = w.duration
    
    return success(
        data={
            "hourly": hourly_data,
            "weekly": weekly_data,
        }
    )


@router.get("/app-ranking")
async def get_app_ranking(
    limit: int = Query(10, ge=1, le=50),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取应用排行"""
    query = db.query(
        AppUsage.app_name,
        func.sum(AppUsage.duration).label("total_duration"),
        func.count(AppUsage.id).label("count"),
    )
    
    if start_date:
        query = query.filter(AppUsage.date >= start_date)
    if end_date:
        query = query.filter(AppUsage.date <= end_date)
    
    results = query.group_by(AppUsage.app_name).order_by(
        func.sum(AppUsage.duration).desc()
    ).limit(limit).all()
    
    return success(
        data=[
            {
                "name": r.app_name,
                "duration": r.total_duration,
                "count": r.count,
            }
            for r in results
        ]
    )


@router.get("/game-ranking")
async def get_game_ranking(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取游戏排行"""
    results = db.query(Game).order_by(Game.total_duration.desc()).limit(limit).all()
    
    return success(
        data=[
            {
                "id": game.id,
                "name": game.name,
                "duration": game.total_duration,
                "session_count": game.session_count,
                "cover_image": game.cover_image,
            }
            for game in results
        ]
    )


@router.get("/comparison")
async def get_comparison(
    type: str = Query("weekday_weekend", description="对比类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取对比分析数据"""
    # 工作日 vs 周末
    # 0=周日, 1=周一, ..., 6=周六
    weekday_avg = db.query(
        func.avg(AppUsage.duration),
    ).filter(
        extract("dow", AppUsage.start_time).in_([1, 2, 3, 4, 5])
    ).scalar() or 0
    
    weekend_avg = db.query(
        func.avg(AppUsage.duration),
    ).filter(
        extract("dow", AppUsage.start_time).in_([0, 6])
    ).scalar() or 0
    
    return success(
        data={
            "weekday_avg": int(weekday_avg),
            "weekend_avg": int(weekend_avg),
        }
    )
