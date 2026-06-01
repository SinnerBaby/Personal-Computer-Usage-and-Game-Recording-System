"""
通用数据模式
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, List
import time


class ApiResponse(BaseModel):
    """统一 API 响应"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[Any] = Field(None, description="数据")
    timestamp: float = Field(default_factory=time.time, description="时间戳")


class PaginatedData(BaseModel):
    """分页数据"""
    list: List[Any] = Field(..., description="数据列表")
    pagination: dict = Field(..., description="分页信息")


class PaginatedResponse(BaseModel):
    """分页响应"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: PaginatedData = Field(..., description="分页数据")
    timestamp: float = Field(default_factory=time.time, description="时间戳")


class DateRangeQuery(BaseModel):
    """日期范围查询"""
    start_date: Optional[str] = Field(None, description="开始日期（YYYY-MM-DD）")
    end_date: Optional[str] = Field(None, description="结束日期（YYYY-MM-DD）")


class ExportRequest(BaseModel):
    """导出请求"""
    data_type: str = Field(..., description="数据类型（apps/games）")
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    format: str = Field("csv", description="导出格式（csv/json）")
