"""
基础页面类
所有页面对象都应该继承此类
"""
from playwright.sync_api import Page, Locator, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from typing import Optional
from utils.logger import logger
from utils.config import Config


class BasePage:
    """基础页面类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = Config.DEFAULT_TIMEOUT
    
    def navigate(self, url: str):
        """导航到指定URL"""
        logger.info(f"导航到: {url}")
        self.page.goto(url, timeout=Config.NAVIGATION_TIMEOUT, wait_until="domcontentloaded")
        # 某些站点（如挑战页/长连接）长期无法达到 networkidle，这里降级为软等待
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except PlaywrightTimeoutError:
            logger.warning("页面未达到 networkidle，继续执行后续步骤")
    
    def click(self, selector: str, timeout: Optional[int] = None):
        """点击元素"""
        logger.debug(f"点击元素: {selector}")
        self.page.click(selector, timeout=timeout or self.timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None):
        """填充输入框"""
        logger.debug(f"填充输入框 {selector}: {value}")
        self.page.fill(selector, value, timeout=timeout or self.timeout)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """获取元素文本"""
        return self.page.locator(selector).inner_text(timeout=timeout or self.timeout)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """检查元素是否可见"""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None):
        """等待元素出现"""
        logger.debug(f"等待元素: {selector}")
        self.page.locator(selector).wait_for(state="visible", timeout=timeout or self.timeout)
    
    def get_element(self, selector: str) -> Locator:
        """获取元素定位器"""
        return self.page.locator(selector)
    
    def screenshot(self, filename: str):
        """截图"""
        filepath = Config.SCREENSHOTS_DIR / filename
        logger.info(f"截图保存到: {filepath}")
        self.page.screenshot(path=str(filepath))
    
    def get_title(self) -> str:
        """获取页面标题"""
        return self.page.title()
    
    def get_url(self) -> str:
        """获取当前URL"""
        return self.page.url
    
    def go_back(self):
        """返回上一页"""
        logger.info("返回上一页")
        self.page.go_back()
    
    def refresh(self):
        """刷新页面"""
        logger.info("刷新页面")
        self.page.reload()
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None):
        """等待URL匹配"""
        logger.debug(f"等待URL匹配: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout or self.timeout)
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None):
        """选择下拉框选项"""
        logger.debug(f"选择下拉框 {selector}: {value}")
        self.page.select_option(selector, value, timeout=timeout or self.timeout)
    
    def check(self, selector: str, timeout: Optional[int] = None):
        """勾选复选框"""
        logger.debug(f"勾选复选框: {selector}")
        self.page.check(selector, timeout=timeout or self.timeout)
    
    def uncheck(self, selector: str, timeout: Optional[int] = None):
        """取消勾选复选框"""
        logger.debug(f"取消勾选复选框: {selector}")
        self.page.uncheck(selector, timeout=timeout or self.timeout)
    
    def hover(self, selector: str, timeout: Optional[int] = None):
        """鼠标悬停"""
        logger.debug(f"鼠标悬停: {selector}")
        self.page.hover(selector, timeout=timeout or self.timeout)
    
    def press_key(self, key: str):
        """按键"""
        logger.debug(f"按键: {key}")
        self.page.keyboard.press(key)
    
    def expect_element_visible(self, selector: str, timeout: Optional[int] = None):
        """断言元素可见"""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout or self.timeout)
    
    def expect_element_hidden(self, selector: str, timeout: Optional[int] = None):
        """断言元素隐藏"""
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout or self.timeout)
    
    def expect_text(self, selector: str, text: str, timeout: Optional[int] = None):
        """断言元素文本"""
        expect(self.page.locator(selector)).to_have_text(text, timeout=timeout or self.timeout)
