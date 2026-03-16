"""
Playwright 配置文件（可选）
如果使用 playwright 命令行工具，可以使用此配置
"""
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

# Playwright 项目配置
# 注意：pytest-playwright 主要使用 conftest.py 中的配置
# 此文件可用于 playwright 命令行工具

PLAYWRIGHT_CONFIG = {
    "base_url": os.getenv("BASE_URL", "https://example.com"),
    "timeout": int(os.getenv("BROWSER_TIMEOUT", "60000")),
    "headless": os.getenv("HEADLESS", "True").lower() == "true",
    "viewport": {
        "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
        "height": int(os.getenv("VIEWPORT_HEIGHT", "1080")),
    },
}

