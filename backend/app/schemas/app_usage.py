"""
应用使用记录数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class AppCategoryBase(BaseModel):
    """应用分类基础模式"""
    name: str = Field(..., max_length=50, description="分类名称")
    icon: Optional[str] = Field(None, max_length=50, description="图标名称")
    color: Optional[str] = Field(None, max_length=20, description="颜色值")
    sort_order: Optional[int] = Field(0, description="排序顺序")


class AppCategoryCreate(AppCategoryBase):
    """创建应用分类"""
    pass


class AppCategoryUpdate(BaseModel):
    """更新应用分类"""
    name: Optional[str] = Field(None, max_length=50, description="分类名称")
    icon: Optional[str] = Field(None, max_length=50, description="图标名称")
    color: Optional[str] = Field(None, max_length=20, description="颜色值")
    sort_order: Optional[int] = Field(None, description="排序顺序")


class AppCategoryResponse(AppCategoryBase):
    """应用分类响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AppUsageBase(BaseModel):
    """应用使用记录基础模式"""
    app_name: str = Field(..., max_length=100, description="应用名称")
    window_title: Optional[str] = Field(None, max_length=500, description="窗口标题")
    process_name: str = Field(..., max_length=100, description="进程名称")
    category_id: Optional[int] = Field(None, description="分类ID")
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    duration: Optional[int] = Field(0, description="使用时长（秒）")
    is_idle: Optional[bool] = Field(False, description="是否闲置")


class AppUsageCreate(AppUsageBase):
    """创建应用使用记录"""
    pass


class AppUsageBatchCreate(BaseModel):
    """批量创建应用使用记录"""
    records: List[AppUsageCreate]


class AppUsageResponse(AppUsageBase):
    """应用使用记录响应"""
    id: int
    date: date
    category: Optional[AppCategoryResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AppUsageQuery(BaseModel):
    """应用使用记录查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    app_name: Optional[str] = Field(None, description="应用名称筛选")
    category_id: Optional[int] = Field(None, description="分类ID筛选")
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    is_idle: Optional[bool] = Field(None, description="是否闲置")
    sort_by: Optional[str] = Field("start_time", description="排序字段")
    sort_order: Optional[str] = Field("desc", description="排序方式（asc/desc）")
