"""
应用记录 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import date
from typing import Optional, List

from app.database import get_db
from app.models.user import User
from app.models.app_usage import AppUsage, AppCategory
from app.schemas.app_usage import AppCategoryCreate, AppCategoryUpdate
from app.utils.dependencies import get_current_user
from app.utils.response import success, paginate

router = APIRouter()


@router.get("")
async def get_app_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    app_name: Optional[str] = None,
    category_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取应用使用记录列表"""
    query = db.query(AppUsage)
    
    # 筛选条件
    if app_name:
        query = query.filter(AppUsage.app_name.ilike(f"%{app_name}%"))
    if category_id:
        query = query.filter(AppUsage.category_id == category_id)
    if start_date:
        query = query.filter(AppUsage.date >= start_date)
    if end_date:
        query = query.filter(AppUsage.date <= end_date)
    
    # 总数
    total = query.count()
    
    # 分页查询
    records = query.order_by(desc(AppUsage.start_time)).offset((page - 1) * page_size).limit(page_size).all()
    
    # 转换为字典
    record_list = []
    for record in records:
        record_list.append({
            "id": record.id,
            "app_name": record.app_name,
            "window_title": record.window_title,
            "process_name": record.process_name,
            "category": {
                "id": record.category.id,
                "name": record.category.name,
                "icon": record.category.icon,
                "color": record.category.color,
            } if record.category else None,
            "start_time": record.start_time.isoformat(),
            "end_time": record.end_time.isoformat() if record.end_time else None,
            "duration": record.duration,
            "is_idle": record.is_idle,
            "date": str(record.date),
        })
    
    return paginate(record_list, total, page, page_size)


@router.get("/categories")
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取应用分类列表"""
    categories = db.query(AppCategory).order_by(AppCategory.sort_order).all()
    return success(
        data=[
            {
                "id": cat.id,
                "name": cat.name,
                "icon": cat.icon,
                "color": cat.color,
                "sort_order": cat.sort_order,
            }
            for cat in categories
        ]
    )


@router.post("/categories")
async def create_category(
    category_data: AppCategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建应用分类"""
    category = AppCategory(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return success(
        data={
            "id": category.id,
            "name": category.name,
            "icon": category.icon,
            "color": category.color,
            "sort_order": category.sort_order,
        }
    )


@router.put("/categories/{category_id}")
async def update_category(
    category_id: int,
    category_data: AppCategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新应用分类"""
    category = db.query(AppCategory).filter(AppCategory.id == category_id).first()
    if not category:
        return {"code": 40401, "message": "分类不存在", "data": None, "timestamp": 0}
    
    update_data = category_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    return success(
        data={
            "id": category.id,
            "name": category.name,
            "icon": category.icon,
            "color": category.color,
            "sort_order": category.sort_order,
        }
    )


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除应用分类"""
    category = db.query(AppCategory).filter(AppCategory.id == category_id).first()
    if not category:
        return {"code": 40401, "message": "分类不存在", "data": None, "timestamp": 0}
    
    db.delete(category)
    db.commit()
    return success(message="删除成功")
