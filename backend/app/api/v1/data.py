"""
数据管理 API
"""
import os
import json
import csv
import io
from datetime import datetime, date
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.app_usage import AppUsage
from app.models.game import Game
from app.utils.dependencies import get_current_user
from app.utils.response import success
from app.config import settings

router = APIRouter()


@router.post("/export")
async def export_data(
    export_params: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """导出数据"""
    data_type = export_params.get("data_type", "apps")
    format_type = export_params.get("format", "csv")
    start_date = export_params.get("start_date")
    end_date = export_params.get("end_date")
    
    if data_type == "apps":
        query = db.query(AppUsage)
        if start_date:
            query = query.filter(AppUsage.date >= start_date)
        if end_date:
            query = query.filter(AppUsage.date <= end_date)
        records = query.all()
        
        if format_type == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["id", "app_name", "process_name", "start_time", "end_time", "duration", "date"])
            for r in records:
                writer.writerow([r.id, r.app_name, r.process_name, r.start_time, r.end_time, r.duration, r.date])
            
            return {
                "code": 200,
                "message": "success",
                "data": {"content": output.getvalue(), "filename": f"app_usage_{datetime.now().strftime('%Y%m%d')}.csv"},
                "timestamp": datetime.now().timestamp(),
            }
        else:
            data = [
                {
                    "id": r.id,
                    "app_name": r.app_name,
                    "process_name": r.process_name,
                    "start_time": r.start_time.isoformat(),
                    "end_time": r.end_time.isoformat() if r.end_time else None,
                    "duration": r.duration,
                    "date": str(r.date),
                }
                for r in records
            ]
            return {
                "code": 200,
                "message": "success",
                "data": {"content": json.dumps(data, ensure_ascii=False), "filename": f"app_usage_{datetime.now().strftime('%Y%m%d')}.json"},
                "timestamp": datetime.now().timestamp(),
            }
    else:
        return {"code": 400, "message": "不支持的数据类型", "data": None, "timestamp": 0}


@router.post("/import")
async def import_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """导入数据"""
    content = await file.read()
    content_str = content.decode("utf-8")
    
    if file.filename.endswith(".json"):
        data = json.loads(content_str)
        imported_count = 0
        
        for item in data:
            app_usage = AppUsage(
                app_name=item.get("app_name"),
                process_name=item.get("process_name"),
                start_time=datetime.fromisoformat(item.get("start_time")),
                end_time=datetime.fromisoformat(item.get("end_time")) if item.get("end_time") else None,
                duration=item.get("duration", 0),
                date=datetime.fromisoformat(item.get("start_time")).date(),
            )
            db.add(app_usage)
            imported_count += 1
        
        db.commit()
        return success(data={"imported_count": imported_count})
    else:
        return {"code": 400, "message": "仅支持 JSON 格式", "data": None, "timestamp": 0}


@router.post("/backup")
async def create_backup(
    current_user: User = Depends(get_current_user),
):
    """创建数据库备份"""
    import shutil
    
    backup_dir = settings.BACKUP_DIR
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # 复制数据库文件
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        return success(data={"backup_file": backup_filename})
    else:
        return {"code": 50001, "message": "数据库文件不存在", "data": None, "timestamp": 0}


@router.get("/backups")
async def get_backup_list(
    current_user: User = Depends(get_current_user),
):
    """获取备份列表"""
    backup_dir = settings.BACKUP_DIR
    
    if not os.path.exists(backup_dir):
        return success(data=[])
    
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith(".db"):
            filepath = os.path.join(backup_dir, filename)
            stat = os.stat(filepath)
            backups.append({
                "filename": filename,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    
    backups.sort(key=lambda x: x["created_at"], reverse=True)
    return success(data=backups)


@router.post("/cleanup")
async def cleanup_data(
    cleanup_params: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """清理历史数据"""
    days = cleanup_params.get("days", 365)
    cutoff_date = date.today() - __import__("datetime").timedelta(days=days)
    
    # 删除旧数据
    deleted_count = db.query(AppUsage).filter(AppUsage.date < cutoff_date).delete()
    db.commit()
    
    return success(data={"deleted_count": deleted_count})
