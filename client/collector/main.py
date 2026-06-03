"""
数据采集客户端主入口
"""
import time
import sys
import signal
from datetime import datetime

from collector.window_monitor import WindowMonitor
from collector.game_detector import GameDetector
from collector.data_sender import DataSender


class CollectorMain:
    """数据采集主循环"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.running = False
        self.window_monitor = WindowMonitor()
        self.game_detector = GameDetector(config_path)
        self.data_sender = DataSender(config_path)
        self.collect_interval = 5  # 采集间隔（秒）
        self.sync_interval = 5   # 同步间隔（秒）
        self.last_sync_time = time.time()
    
    def start(self, username: str = "admin", password: str = "admin123"):
        """启动采集"""
        self.running = True
        print(f"[{datetime.now()}] 数据采集客户端启动")
        
        # 登录获取 Token
        print(f"[{datetime.now()}] 正在登录...")
        if not self.data_sender.login(username, password):
            print(f"[{datetime.now()}] 登录失败，请检查用户名密码或服务器状态")
            return
        print(f"[{datetime.now()}] 登录成功")
        
        # 启动时扫描已有的游戏进程
        self._scan_existing_games()
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                # 采集当前活动窗口信息
                window_info = self.window_monitor.get_active_window_info()
                
                if window_info:
                    # 检测是否为游戏（带 exe 路径）
                    is_game, game_name = self.game_detector.is_game(
                        window_info["process_name"],
                        exe_path=window_info.get("exe_path", ""),
                    )
                    window_info["is_game"] = is_game
                    window_info["game_name"] = game_name
                    
                    # 记录数据
                    self.window_monitor.record_switch(window_info)
                
                # 检查是否需要同步数据
                current_time = time.time()
                if current_time - self.last_sync_time >= self.sync_interval:
                    self._sync_data()
                    self.last_sync_time = current_time
                
                time.sleep(self.collect_interval)
                
        except Exception as e:
            print(f"[{datetime.now()}] 采集异常: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """停止采集"""
        self.running = False
        # 同步剩余数据
        self._sync_data()
        print(f"[{datetime.now()}] 数据采集客户端停止")
    
    def _sync_data(self):
        """同步数据到服务器"""
        records = self.window_monitor.get_records()
        if not records:
            return
        
        # 分离游戏记录和普通应用记录
        game_records = [r for r in records if r.get("is_game")]
        app_records = [r for r in records if not r.get("is_game")]
        
        # 同步游戏记录
        if game_records:
            try:
                self.data_sender.send_game_sessions(game_records)
                print(f"[{datetime.now()}] 同步 {len(game_records)} 条游戏记录")
            except Exception as e:
                print(f"[{datetime.now()}] 游戏记录同步失败: {e}")
        
        # 同步普通应用记录
        if app_records:
            try:
                self.data_sender.send_app_usage(app_records)
                print(f"[{datetime.now()}] 同步 {len(app_records)} 条应用记录")
            except Exception as e:
                print(f"[{datetime.now()}] 应用记录同步失败: {e}")
        
        # 清理已同步的记录
        self.window_monitor.clear_records()
    
    def _scan_existing_games(self):
        """启动时扫描系统中已有的游戏进程（优先选中已打开的窗口作为当前应用）"""
        import psutil
        import win32gui
        import win32process
        try:
            found_games = []
            foreground_pid = None
            
            # 获取当前前台窗口PID
            try:
                fg_hwnd = win32gui.GetForegroundWindow()
                _, foreground_pid = win32process.GetWindowThreadProcessId(fg_hwnd)
            except Exception:
                pass
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    pname = proc.info['name']
                    # 尝试获取 exe 路径
                    exe_path = ""
                    try:
                        exe_path = proc.exe()
                    except Exception:
                        pass
                    if pname:
                        is_game, game_name = self.game_detector.is_game(pname, exe_path=exe_path)
                        if is_game:
                            found_games.append(proc)
                            print(f"[{datetime.now()}] 发现游戏进程: {pname} → {game_name}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # 优先选前台窗口的游戏，否则选最新的
            target_proc = None
            for proc in found_games:
                if proc.info['pid'] == foreground_pid:
                    target_proc = proc
                    break
            
            if not target_proc and found_games:
                # 选最后一个（最新启动的）
                target_proc = found_games[-1]
            
            if target_proc:
                pname = target_proc.info['name']
                # 获取 exe 路径
                exe_path = ""
                try:
                    exe_path = target_proc.exe()
                except Exception:
                    pass
                _, game_name = self.game_detector.is_game(pname, exe_path=exe_path)
                from datetime import timedelta
                self.window_monitor.current_app = {
                    "process_name": pname,
                    "window_title": game_name,
                    "pid": target_proc.info['pid'],
                    "is_game": True,
                    "game_name": game_name,
                    "exe_path": exe_path,
                }
                self.window_monitor.current_start = datetime.now() - timedelta(seconds=3)
                print(f"[{datetime.now()}] 开始追踪当前游戏: {game_name}")
                if exe_path:
                    print(f"[{datetime.now()}] 游戏路径: {exe_path}")
        except Exception as e:
            print(f"[{datetime.now()}] 扫描游戏进程异常: {e}")
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print(f"\n[{datetime.now()}] 收到停止信号，正在关闭...")
        self.stop()
        sys.exit(0)


if __name__ == "__main__":
    collector = CollectorMain()
    collector.start()
