"""
游戏识别模块
"""
import yaml
from typing import Tuple, Optional, Dict, List
from pathlib import Path


# 预置游戏进程名库
KNOWN_GAMES = {
    "鸣潮": ["WutheringWaves.exe", "Client-Win64-Shipping.exe"],
    "原神": ["YuanShen.exe", "GenshinImpact.exe"],
    "崩坏：星穹铁道": ["StarRail.exe"],
    "英雄联盟": ["LeagueClient.exe", "League of Legends.exe"],
    "CS2": ["cs2.exe"],
    "Dota 2": ["dota2.exe"],
    "永劫无间": ["NarakaBladepoint.exe"],
    "Steam 游戏通用": ["steam_app_*.exe"],
}


class GameDetector:
    """游戏检测器"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.known_games = KNOWN_GAMES.copy()
        self._load_custom_games(config_path)
    
    def _load_custom_games(self, config_path: str):
        """从配置文件加载自定义游戏列表"""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    custom_games = config.get("games", {})
                    self.known_games.update(custom_games)
        except Exception:
            pass
    
    def is_game(self, process_name: str) -> Tuple[bool, Optional[str]]:
        """
        检测进程是否为游戏
        
        Args:
            process_name: 进程名称
            
        Returns:
            (是否游戏, 游戏名称)
        """
        process_name_lower = process_name.lower()
        
        for game_name, processes in self.known_games.items():
            for pattern in processes:
                if self._match_process(process_name_lower, pattern.lower()):
                    return True, game_name
        
        # 通用检测：检查是否是已知的游戏引擎进程
        game_engine_processes = [
            "unityplayer.dll",
            "unreal engine",
            "gamemaker",
        ]
        
        for engine in game_engine_processes:
            if engine in process_name_lower:
                return True, "未知游戏"
        
        return False, None
    
    def _match_process(self, process_name: str, pattern: str) -> bool:
        """匹配进程名（支持通配符）"""
        if "*" in pattern:
            # 简单的通配符匹配
            prefix = pattern.split("*")[0]
            suffix = pattern.split("*")[-1]
            return process_name.startswith(prefix) and process_name.endswith(suffix)
        return process_name == pattern
    
    def add_game(self, game_name: str, process_names: List[str]):
        """添加游戏到识别库"""
        self.known_games[game_name] = process_names
    
    def remove_game(self, game_name: str):
        """从识别库移除游戏"""
        if game_name in self.known_games:
            del self.known_games[game_name]
