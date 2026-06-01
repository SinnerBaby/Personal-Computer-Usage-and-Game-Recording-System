"""
应用使用记录模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class AppCategory(Base):
    """应用分类表"""
    __tablename__ = "app_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, comment="分类名称")
    icon = Column(String(50), nullable=True, comment="图标名称")
    color = Column(String(20), nullable=True, comment="颜色值")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联
    apps = relationship("AppUsage", back_populates="category")

    def __repr__(self):
        return f"<AppCategory(id={self.id}, name='{self.name}')>"


class AppUsage(Base):
    """应用使用记录表"""
    __tablename__ = "app_usage"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    app_name = Column(String(100), nullable=False, index=True, comment="应用名称")
    window_title = Column(String(500), nullable=True, comment="窗口标题")
    process_name = Column(String(100), nullable=False, comment="进程名称")
    category_id = Column(Integer, ForeignKey("app_categories.id"), nullable=True, comment="分类ID")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=True, comment="结束时间")
    duration = Column(Integer, default=0, comment="使用时长（秒）")
    is_idle = Column(Boolean, default=False, comment="是否闲置")
    date = Column(Date, nullable=False, index=True, comment="日期")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联
    category = relationship("AppCategory", back_populates="apps")

    def __repr__(self):
        return f"<AppUsage(id={self.id}, app_name='{self.app_name}', duration={self.duration})>"
