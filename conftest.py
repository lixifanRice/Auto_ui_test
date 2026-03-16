"""
pytest 配置文件
提供全局的 fixtures 和测试配置
"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from typing import Generator
import os
import json
from dotenv import load_dotenv
from urllib.parse import urlparse

# 加载环境变量
load_dotenv()


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """浏览器启动参数"""
    return {
        "headless": os.getenv("HEADLESS", "True").lower() == "true",
        "slow_mo": int(os.getenv("SLOW_MO", "0")),
        "timeout": int(os.getenv("BROWSER_TIMEOUT", "60000")),
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """浏览器上下文参数"""
    args = {
        "viewport": {
            "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
            "height": int(os.getenv("VIEWPORT_HEIGHT", "1080")),
        },
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos/" if os.getenv("RECORD_VIDEO", "False").lower() == "true" else None,
    }

    # 应用登录用的 Bearer Token（从 .env 的 AUTH_BEARER 读取）
    auth_bearer = os.getenv("AUTH_BEARER", "").strip()
    if auth_bearer:
        # 如果没有带前缀，则补上 "Bearer "
        if not auth_bearer.lower().startswith("bearer "):
            auth_bearer = f"Bearer {auth_bearer}"
        args["extra_http_headers"] = {"Authorization": auth_bearer}
    return args


@pytest.fixture(scope="function")
def page(browser: Browser, browser_context_args: dict) -> Generator[Page, None, None]:
    """创建新的页面实例
    注意：pytest-playwright 会自动提供 browser fixture
    """
    # 过滤掉 None 值
    context_args = {k: v for k, v in browser_context_args.items() if v is not None}
    context = browser.new_context(**context_args)

    # 如果配置了 Cloudflare Access 的 Cookie 值，则以 Cookie 方式注入
    cf_auth = os.getenv("CF_Authorization")
    base_url = os.getenv("BASE_URL")
    if cf_auth and base_url:
        parsed = urlparse(base_url)
        if parsed.hostname:
            context.add_cookies(
                [
                    {
                        "name": "CF_Authorization",
                        "value": cf_auth,
                        "domain": parsed.hostname,
                        "path": "/",
                        "httpOnly": True,
                        "secure": parsed.scheme == "https",
                    }
                ]
            )

    # 只设置 localStorage.__dc-console__language，不再设置其他语言相关项
    lang_raw = os.getenv("__dc-console__language", "").strip()
    if lang_raw:
        # 如果 .env 中不是合法 JSON，这里兜底成默认中文配置
        try:
            json.loads(lang_raw)
        except json.JSONDecodeError:
            lang_raw = json.dumps({"label": "中文（简体）", "value": "zh-CN"}, ensure_ascii=False)

    if lang_raw:
        page = context.new_page()
        # 旧版本 Playwright 的 add_init_script 只接受一个 script 参数，
        # 这里直接把 .env 中的 JSON 字符串内联进脚本。
        lang_literal = json.dumps(lang_raw)
        init_script = f"""
(() => {{
  try {{
    const langJson = {lang_literal};
    localStorage.setItem('__dc-console__language', langJson);
  }} catch (e) {{}}
}})();
"""
        page.add_init_script(init_script)
    else:
        page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="session")
def base_url():
    """基础URL"""
    return os.getenv("BASE_URL", "https://example.com")


@pytest.fixture(scope="function", autouse=True)
def setup_test(page: Page, base_url: str):
    """每个测试前的设置"""
    # 可以在这里添加通用的测试前设置
    pass


@pytest.fixture(scope="function", autouse=True)
def teardown_test(page: Page, request):
    """每个测试后的清理"""
    yield
    # 测试失败时截图
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        try:
            page.screenshot(path=f"{screenshot_dir}/{request.node.name}.png")
        except Exception as e:
            print(f"截图失败: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在测试报告中记录测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

