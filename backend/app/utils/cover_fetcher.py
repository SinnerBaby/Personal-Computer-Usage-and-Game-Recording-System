"""
Steam 游戏封面抓取引擎
使用标准库 urllib，无需额外依赖
"""
import os
import logging
import re
import urllib.request
import urllib.parse
import json
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

COVERS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "covers"

STEAM_HEADER_URL = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/header.jpg"
STEAM_CAPSULE_URL = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/capsule_231x87.jpg"
STEAM_LIBRARY_URL = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def ensure_covers_dir():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)


def get_steam_appid_from_path(exe_path: str) -> Optional[int]:
    if not exe_path or "steamapps" not in exe_path.lower():
        return None

    exe = Path(exe_path)
    for parent in [exe.parent, exe.parent.parent, exe.parent.parent.parent]:
        appid_file = parent / "steam_appid.txt"
        if appid_file.exists():
            try:
                return int(appid_file.read_text().strip())
            except (ValueError, OSError):
                pass
    return None


def search_steam_appid(game_name: str) -> Optional[int]:
    """通过 Steam 商店搜索页面查找 AppID"""
    try:
        # 尝试 API 搜索（可能被限流）
        params = urllib.parse.urlencode({"term": game_name, "l": "english"})
        url = f"https://store.steampowered.com/api/storesearch?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        resp = urllib.request.urlopen(req, timeout=8)
        data = json.loads(resp.read())
        items = data.get("items", [])
        if items:
            return items[0].get("id")

        # API 失败，尝试搜索页面 HTML 解析
        search_params = urllib.parse.urlencode({"term": game_name, "category1": 998})  # 998=games
        search_url = f"https://store.steampowered.com/search/?{search_params}"
        search_req = urllib.request.Request(
            search_url,
            headers={
                "User-Agent": _UA,
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
        )
        search_resp = urllib.request.urlopen(search_req, timeout=10)
        html = search_resp.read().decode("utf-8", errors="ignore")

        # 在 HTML 中找 appid
        # Steam 搜索结果页的链接格式: https://store.steampowered.com/app/1296830/...
        import re
        pattern = r'/app/(\d+)/'
        # 只取第一个匹配
        matches = re.findall(pattern, html)
        if matches:
            return int(matches[0])
    except Exception as e:
        logger.warning(f"Steam 搜索失败 ({game_name}): {e}")
    return None


def download_cover(appid: int, target_path: Path) -> bool:
    urls = [
        (STEAM_LIBRARY_URL, "library"),
        (STEAM_HEADER_URL, "header"),
        (STEAM_CAPSULE_URL, "capsule"),
    ]

    for url_template, size_name in urls:
        url = url_template.format(appid=appid)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read()
            if len(data) > 1000:
                target_path.write_bytes(data)
                logger.info(f"封面下载成功: {target_path.name} ({size_name})")
                return True
        except Exception as e:
            logger.warning(f"封面下载失败 ({url}): {e}")

    logger.warning(f"所有封面尺寸均下载失败 (appid={appid})")
    return False


def fetch_game_cover(game_name: str, exe_path: str, game_id: int) -> Optional[str]:
    """
    对外接口：获取游戏封面并保存到本地
    返回相对于 data/ 的路径（如 covers/3.jpg），失败返回 None
    """
    ensure_covers_dir()
    target_path = COVERS_DIR / f"{game_id}.jpg"

    if target_path.exists():
        return str(target_path.relative_to(COVERS_DIR.parent))

    # 1. 从 exe 路径读 steam_appid.txt
    appid = get_steam_appid_from_path(exe_path)

    # 2. 搜索 Steam
    if not appid:
        appid = search_steam_appid(game_name)

    # 3. 下载封面
    if appid and download_cover(appid, target_path):
        return str(target_path.relative_to(COVERS_DIR.parent))

    return None
