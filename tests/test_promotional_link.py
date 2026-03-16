"""
回流链接测试用例
测试 DC Console: https://console-test-deepclick.qiliangjia.one/promotional-link
"""
import pytest
import os
from playwright.sync_api import Page
from pages.promotional_link_page import PromotionalLinkPage
from utils.config import Config


@pytest.fixture
def authenticated_page(page: Page):
    """创建已认证的页面上下文"""
    # 获取认证 token
    auth_bearer = os.getenv("AUTH_BEARER", "")
    if auth_bearer:
        # 设置额外的 HTTP 头
        page.set_extra_http_headers({
            "Authorization": auth_bearer
        })
    return page


@pytest.mark.smoke
def test_click_new_return_link_button(authenticated_page: Page):
    """
    测试用例: 点击新建回流链接按钮
    
    步骤:
    1. 打开回流链接页面
    2. 点击新建回流链接按钮
    
    预期:
    - 页面加载成功
    - 按钮点击成功(跳转或弹窗)
    """
    # 1. 打开回流链接页面
    promo_page = PromotionalLinkPage(authenticated_page)
    promo_page.open()
    
    # 等待页面加载
    authenticated_page.wait_for_load_state("domcontentloaded")
    authenticated_page.wait_for_timeout(5000)  # 等待登录跳转
    
    # 截图看看现在页面状态
    authenticated_page.screenshot(path="reports/screenshots/debug_page_state.png")
    
    # 获取当前 URL
    current_url = authenticated_page.url
    print(f"当前页面URL: {current_url}")
    
    # 获取页面文本
    page_text = authenticated_page.text_content("body")[:500] if authenticated_page.text_content("body") else ""
    print(f"页面内容: {page_text[:200]}...")
    
    # 检查是否需要登录 (查看是否有登录相关内容)
    if "登录" in page_text or "login" in page_text.lower():
        print("⚠️ 页面需要登录，请先在浏览器中手动登录后再运行测试")
    
    # 2. 验证页面加载成功
    if not promo_page.is_page_loaded():
        # 再尝试等待一下
        authenticated_page.wait_for_timeout(3000)
    
    assert promo_page.is_page_loaded(), "页面加载失败"
    
    # 3. 点击新建回流链接按钮
    promo_page.click_new_link_button()
    
    # 等待一下看是否有弹窗或跳转
    authenticated_page.wait_for_timeout(2000)
    
    # 截图记录
    authenticated_page.screenshot(path="reports/screenshots/test_click_new_return_link_button.png")
    
    print("测试完成: 新建回流链接按钮点击成功")
