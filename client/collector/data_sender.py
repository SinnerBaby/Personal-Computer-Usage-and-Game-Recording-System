"""
数据发送模块
"""
import requests
import yaml
from typing import List, Dict, Optional
from pathlib import Path


class DataSender:
    """数据发送器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.base_url = "http://localhost:8000/api/v1"
        self.token: Optional[str] = None
        self.timeout = 10
        self._load_config(config_path)
    
    def _load_config(self, config_path: str):
        """加载配置"""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    server_config = config.get("server", {})
                    self.base_url = server_config.get("url", self.base_url)
                    self.timeout = server_config.get("timeout", self.timeout)
        except Exception:
            pass
    
    def login(self, username: str, password: str) -> bool:
        """登录获取 Token"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=self.timeout,
            )
            data = response.json()
            
            if data.get("code") == 200:
                self.token = data["data"]["token"]
                return True
            return False
        except Exception:
            return False
    
    def send_app_usage(self, records: List[Dict]) -> bool:
        """发送应用使用记录"""
        if not self.token:
            raise Exception("未登录，请先调用 login 方法")
        
        try:
            response = requests.post(
                f"{self.base_url}/sync/app-usage",
                json=records,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=self.timeout,
            )
            data = response.json()
            return data.get("code") == 200
        except Exception as e:
            raise Exception(f"发送失败: {e}")
    
    def send_game_sessions(self, sessions: List[Dict]) -> bool:
        """发送游戏游玩记录"""
        if not self.token:
            raise Exception("未登录，请先调用 login 方法")
        
        try:
            response = requests.post(
                f"{self.base_url}/sync/game-sessions",
                json=sessions,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=self.timeout,
            )
            data = response.json()
            return data.get("code") == 200
        except Exception as e:
            raise Exception(f"发送失败: {e}")
    
    def ensure_game_exists(self, game_name: str, process_name: str = "") -> int:
        """确保游戏在数据库中存在，返回 game_id"""
        if not self.token:
            raise Exception("未登录")
        
        try:
            # 检查游戏是否已存在
            params = {"name": game_name, "page": 1, "page_size": 1}
            response = requests.get(
                f"{self.base_url}/games",
                params=params,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=self.timeout,
            )
            data = response.json()
            
            if data.get("code") == 200:
                game_list = data.get("data", {}).get("list", [])
                if game_list:
                    return game_list[0]["id"]
            
            # 游戏不存在，创建
            response = requests.post(
                f"{self.base_url}/games",
                json={
                    "name": game_name,
                    "notes": f"自动识别自进程 {process_name}",
                },
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=self.timeout,
            )
            data = response.json()
            if data.get("code") == 200:
                return data["data"]["id"]
            return 0
        except Exception as e:
            raise Exception(f"创建游戏失败: {e}")
    
    def check_connection(self) -> bool:
        """检查服务器连接"""
        try:
            response = requests.get(
                f"{self.base_url.replace('/api/v1', '')}/health",
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False
