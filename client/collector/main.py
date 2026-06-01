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
        self.sync_interval = 60  # 同步间隔（秒）
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
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                # 采集当前活动窗口信息
                window_info = self.window_monitor.get_active_window_info()
                
                if window_info:
                    # 检测是否为游戏
                    is_game, game_name = self.game_detector.is_game(window_info["process_name"])
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
        if records:
            try:
                self.data_sender.send_app_usage(records)
                self.window_monitor.clear_records()
                print(f"[{datetime.now()}] 同步 {len(records)} 条记录")
            except Exception as e:
                print(f"[{datetime.now()}] 同步失败: {e}")
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print(f"\n[{datetime.now()}] 收到停止信号，正在关闭...")
        self.stop()
        sys.exit(0)


if __name__ == "__main__":
    collector = CollectorMain()
    collector.start()
