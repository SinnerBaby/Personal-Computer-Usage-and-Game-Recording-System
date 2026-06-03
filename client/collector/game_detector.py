"""
游戏识别模块
"""
import os
import yaml
from typing import Tuple, Optional, Dict, List
from pathlib import Path


# 预置游戏进程名库
KNOWN_GAMES = {
    "鸣潮": ["WutheringWaves.exe", "Client-Win64-Shipping.exe"],
    "原神": ["YuanShen.exe", "GenshinImpact.exe"],
    "崩坏：星穹铁道": ["StarRail.exe", "StarRailBase.exe"],
    "崩坏3": ["BH3.exe", "BH3_win64.exe"],
    "绝区零": ["ZZZ.exe"],
    "英雄联盟": ["LeagueClient.exe", "League of Legends.exe", "LeagueClientUx.exe"],
    "CS2": ["cs2.exe", "csgo.exe"],
    "CSGO": ["csgo.exe"],
    "Dota 2": ["dota2.exe"],
    "永劫无间": ["NarakaBladepoint.exe"],
    "Valorant": ["VALORANT.exe", "VALORANT-Win64-Shipping.exe"],
    "守望先锋": ["Overwatch.exe", "Overwatch Launcher.exe"],
    "暗黑破坏神4": ["Diablo IV.exe"],
    "魔兽世界": ["Wow.exe", "WowClassic.exe", "Battle.net.exe"],
    "炉石传说": ["Hearthstone.exe"],
    "命运2": ["destiny2.exe"],
    "APEX英雄": ["r5apex.exe", "EasyAntiCheat_launcher.exe"],
    "使命召唤": ["cod.exe", "BlackOpsColdWar.exe", "ModernWarfare.exe"],
    "战地风云": ["bf2042.exe", "bf5.exe", "bf1.exe"],
    "彩虹六号：围攻": ["RainbowSix.exe", "RainbowSixSiege.exe"],
    "赛博朋克2077": ["Cyberpunk2077.exe"],
    "艾尔登法环": ["EldenRing.exe"],
    "只狼：影逝二度": ["sekiro.exe"],
    "地平线：零之曙光": ["HorizonZeroDawn.exe"],
    "荒野大镖客：救赎2": ["RDR2.exe"],
    "GTA V": ["GTA5.exe", "GTAV.exe"],
    "巫师3": ["witcher3.exe"],
    "文明6": ["CivilizationVI.exe"],
    "城市：天际线": ["Cities.exe", "Cities_Data.exe"],
    "星露谷物语": ["Stardew Valley.exe"],
    "戴森球计划": ["Dyson Sphere Program.exe"],
    "幻兽帕鲁": ["Palworld.exe"],
    "方舟：生存进化": ["ShooterGame.exe"],
    "森林": ["TheForest.exe"],
    "木筏生存": ["Raft.exe"],
    "我的世界": ["javaw.exe", "Minecraft.exe"],
    "泰拉瑞亚": ["Terraria.exe"],
    "异星工厂": ["factorio.exe"],
    "缺氧": ["OxygenNotIncluded.exe"],
    "博德之门3": ["bg3.exe", "BG3_DX11.exe"],
    "星空": ["Starfield.exe"],
    "辐射4": ["Fallout4.exe"],
    "上古卷轴5": ["SkyrimSE.exe", "Skyrim.exe"],
    "怪物猎人：世界": ["MonsterHunterWorld.exe"],
    "怪物猎人：崛起": ["MonsterHunterRise.exe"],
    "只狼：影逝二度": ["Sekiro.exe"],
    "暖雪": ["WarmSnow.exe"],
    "仁王2": ["nioh2.exe"],
    "鬼泣5": ["DevilMayCry5.exe"],
    "最终幻想14": ["ffxiv.exe", "ffxiv_dx11.exe"],
    "最终幻想7重制版": ["ff7remake_.exe"],
    "女神异闻录5皇家版": ["P5R.exe"],
    "歧路旅人2": ["Octopath_Traveler2.exe"],
    "战网": ["Battle.net.exe", "Blizzard Battle.net.exe"],
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
    
    def is_game(self, process_name: str, exe_path: str = "") -> Tuple[bool, Optional[str]]:
        """
        检测进程是否为游戏
        
        Args:
            process_name: 进程名称
            exe_path: 可执行文件完整路径（可选，用于 Steam 路径自动识别）
            
        Returns:
            (是否游戏, 游戏名称)
        """
        process_name_lower = process_name.lower()
        
        # 1. 按预设进程名匹配
        for game_name, processes in self.known_games.items():
            for pattern in processes:
                if self._match_process(process_name_lower, pattern.lower()):
                    return True, game_name
        
        # 2. Steam 路径自动识别：只要在 steamapps/common/ 下就是游戏
        if exe_path and "steamapps" in exe_path.lower() and "common" in exe_path.lower():
            # 从路径提取游戏目录名作为游戏名
            exe_path_lower = exe_path.lower()
            try:
                # steamapps/common/<GameName>/...
                idx = exe_path_lower.index("steamapps" + os.sep + "common" + os.sep)
                start = idx + len("steamapps" + os.sep + "common" + os.sep)
                # 游戏目录名截止到下一个分隔符
                rest = exe_path_lower[start:]
                game_dir = rest.split(os.sep)[0]
                # 用目录名作为游戏名（可读性更好）
                from pathlib import Path as _Path
                game_dir_full = _Path(exe_path).parent
                # 往上找 steamapps/common/ 后的那个目录
                parts = _Path(exe_path).parts
                for i, part in enumerate(parts):
                    if part.lower() == "steamapps":
                        if i + 2 < len(parts):
                            game_name = parts[i + 2]
                            return True, game_name
                return True, game_dir.title()
            except Exception:
                return True, "Steam 游戏"
        
        # 3. 通用检测：游戏引擎进程
        game_engine_keywords = [
            "unityplayer.dll",
            "unreal engine",
            "gamemaker",
        ]
        
        for keyword in game_engine_keywords:
            if keyword in process_name_lower:
                return True, "未知游戏（引擎匹配）"
        
        # 4. 通用检测：Steam 游戏通用进程名模式
        steam_common = [
            "win64_shipping",
            "win32_shipping",
            "easyanticheat",
            "battleye",
        ]
        for keyword in steam_common:
            if keyword in process_name_lower:
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
