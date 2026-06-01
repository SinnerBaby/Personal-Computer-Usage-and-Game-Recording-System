"""
游戏相关模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date, Text, Table
from sqlalchemy.orm import relationship
from app.database import Base

# 游戏-标签关联表
GameTagRelation = Table(
    "game_tag_relations",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("game_tags.id", ondelete="CASCADE"), primary_key=True),
)


class Game(Base):
    """游戏表"""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True, comment="游戏名称")
    developer = Column(String(100), nullable=True, comment="开发商")
    publisher = Column(String(100), nullable=True, comment="发行商")
    platform = Column(String(50), nullable=True, comment="平台（Steam/Epic/PC等）")
    purchase_price = Column(Float, nullable=True, comment="购买价格")
    purchase_date = Column(Date, nullable=True, comment="购买日期")
    cover_image = Column(String(255), nullable=True, comment="封面图路径")
    rating = Column(Float, nullable=True, comment="个人评分（1-10）")
    notes = Column(Text, nullable=True, comment="游玩笔记")
    total_duration = Column(Integer, default=0, comment="总游玩时长（秒）")
    session_count = Column(Integer, default=0, comment="游玩次数")
    last_played_at = Column(DateTime, nullable=True, comment="最后游玩时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关联
    tags = relationship("GameTag", secondary=GameTagRelation, back_populates="games")
    sessions = relationship("GameSession", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, name='{self.name}')>"


class GameTag(Base):
    """游戏标签表"""
    __tablename__ = "game_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, comment="标签名称")
    color = Column(String(20), nullable=True, comment="颜色值")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联
    games = relationship("Game", secondary=GameTagRelation, back_populates="tags")

    def __repr__(self):
        return f"<GameTag(id={self.id}, name='{self.name}')>"


class GameSession(Base):
    """游戏游玩记录表"""
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True, comment="游戏ID")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Integer, default=0, comment="游玩时长（秒）")
    date = Column(Date, nullable=False, index=True, comment="日期")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联
    game = relationship("Game", back_populates="sessions")

    def __repr__(self):
        return f"<GameSession(id={self.id}, game_id={self.game_id}, duration={self.duration})>"
