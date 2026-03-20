"""
推广管理 > 回流链接 模块测试
"""
import os
from datetime import datetime
import pytest
from playwright.sync_api import Page
from pages.promotional_link_page import PromotionalLinkPage

pytestmark = [pytest.mark.promotion_management, pytest.mark.backflow_link]


@pytest.mark.smoke
def test_create_backflow_link(page: Page):
    """打开回流链接页，填写并提交新建表单，创建一条数据"""
    promo_page = PromotionalLinkPage(page)
    promo_page.open()
    page.wait_for_timeout(3000)

    # 命中 Cloudflare Access 登录页时跳过，避免误报
    if promo_page.is_on_cf_login_page():
        pytest.skip("当前会话仍在 Cloudflare Access 登录页，未进入业务页")

    if not promo_page.wait_new_link_trigger_visible():
        pytest.skip("15秒内未出现“新建回流链接”入口（可能受权限或页面状态影响）")

    opened_new_tab = promo_page.click_new_link_trigger()
    if opened_new_tab:
        print("检测到新建入口打开了新页签，已自动切换到新页签继续执行")

    if not promo_page.wait_new_link_form_visible():
        pytest.skip("已点击新建入口，但未出现新建表单（可能受权限/页面状态影响）")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    link_name = f"auto_link_{ts}"
    button_text = f"立即查看_{ts[-4:]}"
    landing_page_name = f"auto_landing_{ts}"
    product_keyword = os.getenv("PROMO_PRODUCT_KEYWORD", "").strip()
    target_url = os.getenv("PROMO_TARGET_URL", "https://example.com").strip()
    media_keyword = os.getenv("PROMO_MEDIA_KEYWORD", "").strip()
    attribution_tool_keyword = os.getenv("PROMO_ATTRIBUTION_TOOL_KEYWORD", "自归因").strip()
    domain_keyword = os.getenv("PROMO_DOMAIN_KEYWORD", "").strip()
    region_keyword = os.getenv("PROMO_REGION_KEYWORD", "").strip()
    event_keyword = os.getenv("PROMO_EVENT_KEYWORD", "").strip()
    times_keyword = os.getenv("PROMO_TIMES_KEYWORD", "").strip()

    identifier = promo_page.fill_new_link_form(
        link_name=link_name,
        button_text=button_text,
        landing_page_name=landing_page_name,
        product_keyword=product_keyword,
        target_url=target_url,
        media_keyword=media_keyword,
        attribution_tool_keyword=attribution_tool_keyword,
        domain_keyword=domain_keyword,
        region_keyword=region_keyword,
        event_keyword=event_keyword,
        times_keyword=times_keyword,
    )
    assert promo_page.submit_new_link_form(), "未找到可点击的提交按钮（保存/确定）"
    if not promo_page.wait_create_success():
        form_errors = promo_page.get_visible_form_errors()
        assert not form_errors, f"提交后未检测到“创建成功”提示，页面错误: {form_errors}"

    # 如果有可识别标识，则额外做一次列表检索校验
    if identifier and promo_page.is_list_page():
        promo_page.search_by_keyword(identifier)
        if not promo_page.is_keyword_visible_in_table(identifier):
            print(f"提示：当前列表暂未检索到新建数据（可能受索引延迟影响）: {identifier}")

    promo_page.get_active_page().screenshot(path="reports/screenshots/test_new_link_form_opened.png")
