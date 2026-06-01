"""
统一响应封装
"""
from typing import Any, Optional
import time


def success(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return {
        "code": 200,
        "message": message,
        "data": data,
        "timestamp": time.time(),
    }


def error(code: int, message: str) -> dict:
    """错误响应"""
    return {
        "code": code,
        "message": message,
        "data": None,
        "timestamp": time.time(),
    }


def paginate(list_data: list, total: int, page: int, page_size: int) -> dict:
    """分页响应"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": list_data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size,
            },
        },
        "timestamp": time.time(),
    }
