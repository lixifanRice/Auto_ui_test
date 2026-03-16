"""
配置管理类
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()


class Config:
    """配置类"""
    
    # 项目根目录
    PROJECT_ROOT = Path(__file__).parent.parent
    
    # 基础URL
    BASE_URL = os.getenv("BASE_URL", "https://www.baidu.com")
    
    # 浏览器配置
    HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "60000"))
    
    # 视口配置
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # 测试数据
    TEST_USERNAME = os.getenv("TEST_USERNAME", "test_user")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "test_password")
    
    # 目录配置
    REPORTS_DIR = PROJECT_ROOT / "reports"
    SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
    VIDEOS_DIR = REPORTS_DIR / "videos"
    LOGS_DIR = PROJECT_ROOT / "logs"
    TEST_DATA_DIR = PROJECT_ROOT / "test_data"
    
    # 超时配置
    DEFAULT_TIMEOUT = 30000  # 30秒
    NAVIGATION_TIMEOUT = 60000  # 60秒
    
    @classmethod
    def setup_directories(cls):
        """创建必要的目录"""
        directories = [
            cls.REPORTS_DIR,
            cls.SCREENSHOTS_DIR,
            cls.VIDEOS_DIR,
            cls.LOGS_DIR,
            cls.TEST_DATA_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# 初始化目录
Config.setup_directories()

