"""
示例测试用例
"""
import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from utils.config import Config


@pytest.mark.smoke
def test_example_basic(page: Page):
    """基础示例测试"""
    # 导航到页面
    page.goto(Config.BASE_URL)
    page.wait_for_timeout(10000)
    # 验证页面标题
    assert page.title() is not None
    
    # 截图
    page.screenshot(path="reports/screenshots/example_basic.png")

@pytest.mark.skip(reason="示例用例，暂时跳过")
@pytest.mark.smoke
def test_home_page_navigation(page: Page):
    """首页导航测试"""
    home_page = HomePage(page)
    home_page.open()
    
    # 验证页面加载
    assert home_page.get_title() is not None
    assert Config.BASE_URL in home_page.get_url()

@pytest.mark.skip(reason="示例用例，暂时跳过")
@pytest.mark.regression
def test_page_interaction(page: Page):
    """页面交互测试示例"""
    home_page = HomePage(page)
    home_page.open()
    
    # 检查导航菜单
    if home_page.is_navigation_visible():
        # 执行一些交互操作
        pass
    
    # 验证页面状态
    assert home_page.get_url() is not None

@pytest.mark.skip(reason="示例用例，暂时跳过")
@pytest.mark.parametrize("keyword", ["test1", "test2", "test3"])
def test_search_functionality(page: Page, keyword: str):
    """参数化测试示例"""
    home_page = HomePage(page)
    home_page.open()
    
    # 执行搜索（如果页面有搜索功能）
    # home_page.search(keyword)
    
    # 验证结果
    assert page.url is not None

