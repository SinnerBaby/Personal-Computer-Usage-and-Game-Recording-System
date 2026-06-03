"""
窗口监控模块
"""
import psutil
from datetime import datetime
from typing import Optional, Dict, List


class WindowMonitor:
    """窗口监控器"""
    
    def __init__(self, idle_threshold: int = 300):
        self.idle_threshold = idle_threshold  # 闲置阈值（秒）
        self.current_app: Optional[Dict] = None
        self.current_start: Optional[datetime] = None
        self.records: List[Dict] = []
    
    def get_active_window_info(self) -> Optional[Dict]:
        """获取当前前台窗口信息"""
        try:
            import win32gui
            import win32process
            
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            title = win32gui.GetWindowText(hwnd)
            
            if not title:  # 无标题窗口通常是系统窗口
                return None
            
            process = psutil.Process(pid)
            
            return {
                "process_name": process.name(),
                "window_title": title,
                "pid": pid,
                "exe_path": process.exe(),  # 可执行文件完整路径
            }
        except Exception:
            return None
    
    def record_switch(self, new_info: Dict):
        """处理应用切换，记录使用数据"""
        now = datetime.now()
        
        if self.current_app:
            # 如果切换了应用
            if self.current_app["process_name"] != new_info["process_name"]:
                duration = int((now - self.current_start).total_seconds())
                
                # 只记录超过 1 秒的使用
                if duration > 1:
                    self.records.append({
                        "process_name": self.current_app["process_name"],
                        "app_name": self._extract_app_name(self.current_app["window_title"]),
                        "window_title": self.current_app["window_title"],
                        "start_time": self.current_start.isoformat(),
                        "end_time": now.isoformat(),
                        "duration": duration,
                        "is_idle": False,
                        "is_game": self.current_app.get("is_game", False),
                        "game_name": self.current_app.get("game_name"),
                        "exe_path": self.current_app.get("exe_path"),
                    })
                
                # 更新当前应用
                self.current_app = new_info
                self.current_start = now
        else:
            # 第一次记录
            self.current_app = new_info
            self.current_start = now
    
    def get_records(self) -> List[Dict]:
        """获取待同步的记录"""
        # 添加当前正在使用的应用记录
        if self.current_app and self.current_start:
            now = datetime.now()
            duration = int((now - self.current_start).total_seconds())
            
            if duration > 1:
                self.records.append({
                    "process_name": self.current_app["process_name"],
                    "app_name": self._extract_app_name(self.current_app["window_title"]),
                    "window_title": self.current_app["window_title"],
                    "start_time": self.current_start.isoformat(),
                    "end_time": now.isoformat(),
                    "duration": duration,
                    "is_idle": False,
                    "is_game": self.current_app.get("is_game", False),
                    "game_name": self.current_app.get("game_name"),
                    "exe_path": self.current_app.get("exe_path"),
                })
                # 重置当前应用记录
                self.current_start = now
        
        return self.records.copy()
    
    def clear_records(self):
        """清空已同步的记录"""
        self.records.clear()
    
    def _extract_app_name(self, window_title: str) -> str:
        """从窗口标题提取应用名称"""
        # 常见模式：应用名 - 文档名 或 文档名 - 应用名
        separators = [" - ", " – ", " — ", " | "]
        
        for sep in separators:
            if sep in window_title:
                parts = window_title.split(sep)
                # 通常应用名在最后或最前
                # 返回较长的部分作为应用名（通常是文档名）
                # 这里简化处理，返回整个标题
                return window_title
        
        return window_title
