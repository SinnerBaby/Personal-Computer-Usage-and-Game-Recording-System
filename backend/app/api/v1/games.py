"""
游戏记录 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from datetime import date
from typing import Optional, List

from app.database import get_db
from app.models.user import User
from app.models.game import Game, GameTag, GameSession, GameTagRelation
from app.schemas.game import GameCreate, GameUpdate, GameTagCreate, GameSessionCreate
from app.utils.dependencies import get_current_user
from app.utils.response import success, paginate

router = APIRouter()


@router.get("")
async def get_game_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    name: Optional[str] = None,
    platform: Optional[str] = None,
    sort_by: Optional[str] = "last_played_at",
    sort_order: Optional[str] = "desc",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取游戏列表"""
    query = db.query(Game).options(joinedload(Game.tags))
    
    # 筛选条件
    if name:
        query = query.filter(Game.name.ilike(f"%{name}%"))
    if platform:
        query = query.filter(Game.platform == platform)
    
    # 去重（因为 joinedload 可能产生重复）
    query = query.distinct()
    
    # 总数
    total = query.count()
    
    # 排序
    order_column = getattr(Game, sort_by, Game.last_played_at)
    if sort_order == "desc":
        query = query.order_by(desc(order_column))
    else:
        query = query.order_by(order_column)
    
    # 分页查询
    games = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 转换为字典
    game_list = []
    for game in games:
        game_list.append({
            "id": game.id,
            "name": game.name,
            "developer": game.developer,
            "publisher": game.publisher,
            "platform": game.platform,
            "purchase_price": game.purchase_price,
            "purchase_date": str(game.purchase_date) if game.purchase_date else None,
            "cover_image": game.cover_image,
            "rating": game.rating,
            "notes": game.notes,
            "total_duration": game.total_duration,
            "session_count": game.session_count,
            "last_played_at": game.last_played_at.isoformat() if game.last_played_at else None,
            "tags": [{"id": tag.id, "name": tag.name, "color": tag.color} for tag in game.tags],
            "created_at": game.created_at.isoformat(),
            "updated_at": game.updated_at.isoformat(),
        })
    
    return paginate(game_list, total, page, page_size)


@router.get("/tags")
async def get_game_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取游戏标签列表"""
    tags = db.query(GameTag).all()
    return success(
        data=[{"id": tag.id, "name": tag.name, "color": tag.color} for tag in tags]
    )


@router.post("/tags")
async def create_game_tag(
    tag_data: GameTagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建游戏标签"""
    tag = GameTag(**tag_data.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return success(data={"id": tag.id, "name": tag.name, "color": tag.color})


@router.get("/{game_id}")
async def get_game_detail(
    game_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取游戏详情"""
    game = db.query(Game).options(joinedload(Game.tags)).filter(Game.id == game_id).first()
    if not game:
        return {"code": 40401, "message": "游戏不存在", "data": None, "timestamp": 0}
    
    return success(
        data={
            "id": game.id,
            "name": game.name,
            "developer": game.developer,
            "publisher": game.publisher,
            "platform": game.platform,
            "purchase_price": game.purchase_price,
            "purchase_date": str(game.purchase_date) if game.purchase_date else None,
            "cover_image": game.cover_image,
            "rating": game.rating,
            "notes": game.notes,
            "total_duration": game.total_duration,
            "session_count": game.session_count,
            "last_played_at": game.last_played_at.isoformat() if game.last_played_at else None,
            "tags": [{"id": tag.id, "name": tag.name, "color": tag.color} for tag in game.tags],
            "created_at": game.created_at.isoformat(),
            "updated_at": game.updated_at.isoformat(),
        }
    )


@router.post("")
async def create_game(
    game_data: GameCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建游戏"""
    # 创建游戏
    game_dict = game_data.model_dump(exclude={"tag_ids"})
    game = Game(**game_dict)
    
    # 添加标签
    if game_data.tag_ids:
        tags = db.query(GameTag).filter(GameTag.id.in_(game_data.tag_ids)).all()
        game.tags = tags
    
    db.add(game)
    db.commit()
    db.refresh(game)
    
    return success(
        data={
            "id": game.id,
            "name": game.name,
            "tags": [{"id": tag.id, "name": tag.name, "color": tag.color} for tag in game.tags],
        }
    )


@router.put("/{game_id}")
async def update_game(
    game_id: int,
    game_data: GameUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新游戏"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return {"code": 40401, "message": "游戏不存在", "data": None, "timestamp": 0}
    
    # 更新字段
    update_dict = game_data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_dict.items():
        setattr(game, key, value)
    
    # 更新标签
    if game_data.tag_ids is not None:
        tags = db.query(GameTag).filter(GameTag.id.in_(game_data.tag_ids)).all()
        game.tags = tags
    
    db.commit()
    db.refresh(game)
    
    return success(message="更新成功")


@router.delete("/{game_id}")
async def delete_game(
    game_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除游戏"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return {"code": 40401, "message": "游戏不存在", "data": None, "timestamp": 0}
    
    db.delete(game)
    db.commit()
    return success(message="删除成功")


@router.get("/{game_id}/sessions")
async def get_game_sessions(
    game_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取游戏游玩记录"""
    query = db.query(GameSession).filter(GameSession.game_id == game_id)
    total = query.count()
    sessions = query.order_by(desc(GameSession.start_time)).offset((page - 1) * page_size).limit(page_size).all()
    
    session_list = [
        {
            "id": session.id,
            "game_id": session.game_id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration": session.duration,
            "date": str(session.date),
        }
        for session in sessions
    ]
    
    return paginate(session_list, total, page, page_size)


@router.post("/{game_id}/sessions")
async def add_game_session(
    game_id: int,
    session_data: GameSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """添加游戏游玩记录"""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        return {"code": 40401, "message": "游戏不存在", "data": None, "timestamp": 0}
    
    session = GameSession(
        game_id=game_id,
        start_time=session_data.start_time,
        end_time=session_data.end_time,
        duration=session_data.duration,
        date=session_data.start_time.date(),
    )
    db.add(session)
    
    # 更新游戏统计
    game.total_duration += session_data.duration
    game.session_count += 1
    game.last_played_at = session_data.start_time
    
    db.commit()
    db.refresh(session)
    
    return success(
        data={
            "id": session.id,
            "game_id": session.game_id,
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration": session.duration,
            "date": str(session.date),
        }
    )
