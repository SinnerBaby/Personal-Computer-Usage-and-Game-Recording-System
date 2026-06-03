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
from app.utils.cover_fetcher import fetch_game_cover

import threading


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
    """同步游戏游玩记录（自动创建不存在的游戏）"""
    synced_count = 0
    
    for session_data in sessions:
        # 获取 game_id：优先用传进来的，否则按游戏名查找或创建
        game_id = session_data.get("game_id")
        game_name = session_data.get("game_name") or session_data.get("app_name")
        
        if not game_id and game_name:
            # 按名字查找已有游戏
            game = db.query(Game).filter(Game.name == game_name).first()
            if not game:
                # 自动创建新游戏
                exe_path = session_data.get("exe_path", "")
                game = Game(
                    name=game_name,
                    notes=f"采集端自动创建",
                    exe_path=exe_path or None,
                )
                db.add(game)
                db.flush()

                # 后台抓取 Steam 封面
                if exe_path:
                    threading.Thread(
                        target=_fetch_cover_bg,
                        args=(game_name, exe_path, game.id),
                        daemon=True,
                    ).start()
            else:
                # 已有游戏但缺少 exe_path，补充
                exe_path = session_data.get("exe_path", "")
                if exe_path and not game.exe_path:
                    game.exe_path = exe_path
                    db.flush()
                    # 如果也没有封面，尝试抓取
                    if not game.cover_image:
                        threading.Thread(
                            target=_fetch_cover_bg,
                            args=(game_name, exe_path, game.id),
                            daemon=True,
                        ).start()
            game_id = game.id
        
        if not game_id:
            continue
        
        # 确认游戏存在
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            continue
        
        start_time = datetime.fromisoformat(session_data.get("start_time"))
        end_time = datetime.fromisoformat(session_data.get("end_time")) if session_data.get("end_time") else None
        duration = session_data.get("duration", 0)
        
        session = GameSession(
            game_id=game_id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            date=start_time.date(),
        )
        db.add(session)
        
        # 更新游戏统计
        game.total_duration = (game.total_duration or 0) + duration
        game.session_count = (game.session_count or 0) + 1
        game.last_played_at = start_time
        
        synced_count += 1
    
    db.commit()
    
    return success(
        data={
            "synced_count": synced_count,
        }
    )


def _fetch_cover_bg(game_name: str, exe_path: str, game_id: int):
    """后台抓取游戏封面（线程内运行）"""
    from app.database import SessionLocal
    try:
        cover_rel_path = fetch_game_cover(game_name, exe_path, game_id)
        if cover_rel_path:
            db = SessionLocal()
            try:
                game = db.query(Game).filter(Game.id == game_id).first()
                if game:
                    game.cover_image = cover_rel_path
                    db.commit()
            finally:
                db.close()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"封面抓取失败 ({game_name}): {e}")
