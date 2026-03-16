"""
首页页面对象
示例页面对象，可根据实际项目修改
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """首页页面对象"""
    
    # 页面元素定位器
    SEARCH_INPUT = "input[name='q']"
    SEARCH_BUTTON = "button[type='submit']"
    NAVIGATION_MENU = "nav"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "/"
    
    def open(self):
        """打开首页"""
        from utils.config import Config
        self.navigate(Config.BASE_URL + self.url)
    
    def search(self, keyword: str):
        """搜索功能"""
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
    
    def is_navigation_visible(self) -> bool:
        """检查导航菜单是否可见"""
        return self.is_visible(self.NAVIGATION_MENU)

