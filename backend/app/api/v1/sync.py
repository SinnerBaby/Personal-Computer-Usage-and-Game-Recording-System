"""
数据同步 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.app_usage import AppUsage
from app.models.game import Game, GameSession
from app.utils.dependencies import get_current_user
from app.utils.response import success

router = APIRouter()


@router.post("/app-usage")
async def sync_app_usage(
    records: List[dict],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """同步应用使用记录"""
    synced_count = 0
    
    for record in records:
        app_usage = AppUsage(
            app_name=record.get("app_name"),
            window_title=record.get("window_title"),
            process_name=record.get("process_name"),
            start_time=datetime.fromisoformat(record.get("start_time")),
            end_time=datetime.fromisoformat(record.get("end_time")) if record.get("end_time") else None,
            duration=record.get("duration", 0),
            is_idle=record.get("is_idle", False),
            date=datetime.fromisoformat(record.get("start_time")).date(),
        )
        db.add(app_usage)
        synced_count += 1
    
    db.commit()
    
    return success(
        data={
            "synced_count": synced_count,
        }
    )


@router.post("/game-sessions")
async def sync_game_sessions(
    sessions: List[dict],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """同步游戏游玩记录"""
    synced_count = 0
    
    for session_data in sessions:
        game_id = session_data.get("game_id")
        game = db.query(Game).filter(Game.id == game_id).first()
        
        if not game:
            continue
        
        session = GameSession(
            game_id=game_id,
            start_time=datetime.fromisoformat(session_data.get("start_time")),
            end_time=datetime.fromisoformat(session_data.get("end_time")) if session_data.get("end_time") else None,
            duration=session_data.get("duration", 0),
            date=datetime.fromisoformat(session_data.get("start_time")).date(),
        )
        db.add(session)
        
        # 更新游戏统计
        game.total_duration += session_data.get("duration", 0)
        game.session_count += 1
        game.last_played_at = datetime.fromisoformat(session_data.get("start_time"))
        
        synced_count += 1
    
    db.commit()
    
    return success(
        data={
            "synced_count": synced_count,
        }
    )
