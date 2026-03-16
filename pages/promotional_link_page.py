"""
回流链接页面 - Page Object
DC Console: https://console-test-deepclick.qiliangjia.one/promotional-link
"""
from pages.base_page import BasePage
from playwright.sync_api import Page


class PromotionalLinkPage(BasePage):
    """回流链接页面对象"""
    
    # URL
    url = "/promotional-link"
    
    # Auth header for API calls
    AUTH_HEADER = "Authorization"
    
    # 页面元素定位器
    NEW_LINK_BUTTON = "button.sp-button__primary:has-text('新建回流链接')"
    SEARCH_INPUT_LINK_NAME = "input[placeholder='请输入链接名称或ID']"
    SEARCH_INPUT_PRODUCT_NAME = "input[placeholder='请输入产品名称或产品ID']"
    LINK_TABLE = "table.arco-table"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def open(self):
        """打开回流链接页面"""
        from utils.config import Config
        base_url = Config.BASE_URL.rstrip('/')  # 去掉末尾斜杠
        self.navigate(base_url + self.url)
    
    def click_new_link_button(self):
        """点击新建回流链接按钮"""
        self.click(self.NEW_LINK_BUTTON)
    
    def search_by_link_name(self, name: str):
        """根据链接名称搜索"""
        self.fill(self.SEARCH_INPUT_LINK_NAME, name)
    
    def search_by_product_name(self, name: str):
        """根据产品名称搜索"""
        self.fill(self.SEARCH_INPUT_PRODUCT_NAME, name)
    
    def is_page_loaded(self) -> bool:
        """检查页面是否加载完成"""
        return self.is_visible(self.LINK_TABLE)
