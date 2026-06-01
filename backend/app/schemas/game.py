"""
游戏相关数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class GameTagBase(BaseModel):
    """游戏标签基础模式"""
    name: str = Field(..., max_length=50, description="标签名称")
    color: Optional[str] = Field(None, max_length=20, description="颜色值")


class GameTagCreate(GameTagBase):
    """创建游戏标签"""
    pass


class GameTagResponse(GameTagBase):
    """游戏标签响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GameBase(BaseModel):
    """游戏基础模式"""
    name: str = Field(..., max_length=100, description="游戏名称")
    developer: Optional[str] = Field(None, max_length=100, description="开发商")
    publisher: Optional[str] = Field(None, max_length=100, description="发行商")
    platform: Optional[str] = Field(None, max_length=50, description="平台")
    purchase_price: Optional[float] = Field(None, ge=0, description="购买价格")
    purchase_date: Optional[date] = Field(None, description="购买日期")
    cover_image: Optional[str] = Field(None, description="封面图路径")
    rating: Optional[float] = Field(None, ge=1, le=10, description="个人评分（1-10）")
    notes: Optional[str] = Field(None, description="游玩笔记")


class GameCreate(GameBase):
    """创建游戏"""
    tag_ids: Optional[List[int]] = Field([], description="标签ID列表")


class GameUpdate(BaseModel):
    """更新游戏"""
    name: Optional[str] = Field(None, max_length=100, description="游戏名称")
    developer: Optional[str] = Field(None, max_length=100, description="开发商")
    publisher: Optional[str] = Field(None, max_length=100, description="发行商")
    platform: Optional[str] = Field(None, max_length=50, description="平台")
    purchase_price: Optional[float] = Field(None, ge=0, description="购买价格")
    purchase_date: Optional[date] = Field(None, description="购买日期")
    cover_image: Optional[str] = Field(None, description="封面图路径")
    rating: Optional[float] = Field(None, ge=1, le=10, description="个人评分（1-10）")
    notes: Optional[str] = Field(None, description="游玩笔记")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")


class GameSessionBase(BaseModel):
    """游戏游玩记录基础模式"""
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    duration: Optional[int] = Field(0, description="游玩时长（秒）")


class GameSessionCreate(GameSessionBase):
    """创建游戏游玩记录"""
    pass


class GameSessionResponse(GameSessionBase):
    """游戏游玩记录响应"""
    id: int
    game_id: int
    date: date
    created_at: datetime

    class Config:
        from_attributes = True


class GameResponse(GameBase):
    """游戏响应"""
    id: int
    total_duration: int
    session_count: int
    last_played_at: Optional[datetime] = None
    tags: List[GameTagResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GameQuery(BaseModel):
    """游戏查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    name: Optional[str] = Field(None, description="游戏名称筛选")
    platform: Optional[str] = Field(None, description="平台筛选")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID筛选")
    sort_by: Optional[str] = Field("last_played_at", description="排序字段")
    sort_order: Optional[str] = Field("desc", description="排序方式（asc/desc）")
