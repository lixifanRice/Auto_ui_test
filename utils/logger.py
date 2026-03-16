"""
日志工具类
"""
import logging
import os
from datetime import datetime


class Logger:
    """日志工具类"""
    
    def __init__(self, name: str = "playwright_test"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 创建logs目录
            os.makedirs("logs", exist_ok=True)
            
            # 文件handler
            file_handler = logging.FileHandler(
                f"logs/test_{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            
            # 控制台handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误日志"""
        self.logger.critical(message)


# 创建全局logger实例
logger = Logger()

