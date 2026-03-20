"""
回流链接页面对象（POM）
"""
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage
from utils.config import Config


class PromotionalLinkPage(BasePage):
    """回流链接页面对象"""

    PAGE_PATH = "/promotional-link"

    # Cloudflare Access 登录页判定
    CF_LOGIN_URL_MARKER = "cloudflareaccess.com/cdn-cgi/access/login"
    CF_LOGIN_TITLE_MARKERS = ("sign in", "cloudflare access")

    # 新建入口与表单容器
    NEW_LINK_TRIGGER = "div.sp-button:has-text('新建回流链接')"
    NEW_LINK_TRIGGER_WAIT_TIMEOUT_MS = 15000
    NEW_LINK_FORM_CONTAINER = (
        ".arco-modal:visible, "
        "[role='dialog']:visible, "
        ".arco-drawer:visible, "
        ".arco-drawer-content:visible"
    )
    NEW_LINK_FORM_READY = (
        f"{NEW_LINK_FORM_CONTAINER}, "
        "input[placeholder*='请选择产品']:visible, "
        "input[placeholder*='请输入链接名称']:visible, "
        "input[placeholder*='请输入目标页面URL']:visible, "
        "button:has-text('发布'):visible, "
        "input[placeholder*='请选择产品']:visible, "
        "input[placeholder*='按钮文案']:visible, "
        "input[placeholder*='落地页名称']:visible, "
        "button:has-text('保存'):visible"
    )
    NEW_LINK_FORM_WAIT_TIMEOUT_MS = 10000

    LINK_NAME_INPUT_SELECTORS = [
        "input[placeholder*='链接名称']",
        "input[placeholder*='回流链接名称']",
        "input[placeholder*='请输入链接名称']",
    ]
    PRODUCT_INPUT_SELECTORS = [
        "input[placeholder*='请选择产品']",
        "input[placeholder*='产品名称']",
        "input[placeholder*='产品ID']",
    ]
    MEDIA_INPUT_SELECTORS = [
        "input[placeholder*='请选择投放媒体']",
    ]
    ATTRIBUTION_TOOL_INPUT_SELECTORS = [
        "input[placeholder*='选择使用归因工具']",
        "input[placeholder*='请选择归因工具']",
    ]
    ATTRIBUTION_CLICK_URL_INPUT_SELECTORS = [
        "input[placeholder*='点击URL']",
        "input[placeholder*='后台生成的点击URL']",
        "input[placeholder*='Adjust后台生成的点击URL']",
    ]
    DOMAIN_INPUT_SELECTORS = [
        "input[placeholder*='请选择可用域名']",
        "input[placeholder*='一个绿盾链接对应一个域名']",
    ]
    REGION_INPUT_SELECTORS = [
        "input[placeholder*='请选择要投放的地区分级']",
    ]
    EVENT_INPUT_SELECTORS = [
        "input[placeholder*='请选择事件']",
    ]
    TIMES_INPUT_SELECTORS = [
        "input[placeholder*='请选择次数']",
    ]
    REFLUX_LANDING_SELECTORS = [
        "input[placeholder*='请选择回流落地页']",
        "input[placeholder*='回流落地页']",
    ]
    REFLUX_LANDING_CARD_SELECTORS = [
        ".backflow-card-wrapper:has-text('请选择回流落地页') .backflow-card",
        "xpath=//div[contains(@class,'backflow-card-wrapper') and contains(normalize-space(.), '请选择回流落地页')]//div[contains(@class,'backflow-card')]",
    ]
    REFLUX_DRAWER_SELECTORS = [
        ".arco-drawer:visible",
    ]
    REFLUX_DRAWER_ITEM_SELECTORS = [
        ".arco-drawer:visible .content-list-item:visible",
        ".arco-drawer:visible [class*='content-list-item']:visible",
    ]
    REFLUX_DRAWER_CONFIRM_SELECTORS = [
        ".arco-drawer:visible button:has-text('确定')",
        ".arco-drawer:visible .arco-btn-primary:has-text('确定')",
    ]
    COMPLAINT_SWITCH_SELECTORS = [
        "xpath=//div[contains(@class,'items-center') and contains(@class,'font-bold') and contains(normalize-space(.), '投诉回流设置')]//button[@role='switch']",
        "xpath=//div[contains(normalize-space(.), '投诉回流设置')]/button[@role='switch']",
    ]
    TARGET_URL_INPUT_SELECTORS = [
        "input[placeholder*='请输入目标页面URL']",
        "input[placeholder*='目标页面URL']",
        "textarea[placeholder*='请输入目标页面URL']",
    ]
    BUTTON_TEXT_INPUT_SELECTORS = [
        "input[placeholder*='按钮文案']",
        "input[placeholder*='按钮名称']",
    ]
    LANDING_NAME_INPUT_SELECTORS = [
        "input[placeholder*='落地页名称']",
        "input[placeholder*='请输入链接名称']",
    ]
    REMARK_INPUT_SELECTORS = [
        "input[placeholder*='请输入备注']",
    ]

    SUBMIT_BUTTON_SELECTORS = [
        "button:has-text('发布')",
        "button:has-text('保存')",
        "button:has-text('确定')",
        "button:has-text('创建')",
        "button:has-text('提交')",
        "div.sp-button:has-text('保存')",
        "div.sp-button:has-text('确定')",
    ]
    SUCCESS_MESSAGE_SELECTORS = [
        ".arco-message-notice:has-text('成功')",
        ".arco-message:has-text('成功')",
        ".arco-notification:has-text('成功')",
    ]
    SEARCH_INPUT = "input[placeholder='请输入链接名称或ID']"
    TABLE_SELECTOR = ".arco-table"

    def __init__(self, page: Page):
        super().__init__(page)
        self._active_page = page

    def open(self):
        """打开回流链接页"""
        base_url = Config.BASE_URL.rstrip("/")
        self._active_page = self.page
        self.navigate(f"{base_url}{self.PAGE_PATH}")

    def get_active_page(self) -> Page:
        """当前业务操作页（可能是新开页签）"""
        return self._active_page

    def is_on_cf_login_page(self) -> bool:
        """是否处于 Cloudflare Access 登录页"""
        current_url = self._active_page.url.lower()
        title = self._active_page.title().lower()
        return self.CF_LOGIN_URL_MARKER in current_url or (
            self.CF_LOGIN_TITLE_MARKERS[0] in title
            and self.CF_LOGIN_TITLE_MARKERS[1] in title
        )

    def wait_new_link_trigger_visible(self) -> bool:
        """等待新建入口可见"""
        try:
            self._active_page.locator(self.NEW_LINK_TRIGGER).first.wait_for(
                state="visible",
                timeout=self.NEW_LINK_TRIGGER_WAIT_TIMEOUT_MS,
            )
            return True
        except PlaywrightTimeoutError:
            return False

    def click_new_link_trigger(self) -> bool:
        """点击新建入口，若打开新页签则自动切换；返回是否新开页签"""
        trigger = self._active_page.locator(self.NEW_LINK_TRIGGER).first
        try:
            with self._active_page.expect_popup(timeout=5000) as popup_info:
                trigger.click(timeout=self.timeout)
            popup = popup_info.value
            popup.wait_for_load_state("domcontentloaded")
            self._active_page = popup
            return True
        except PlaywrightTimeoutError:
            trigger.click(timeout=self.timeout)
            self._active_page.wait_for_timeout(1000)
            return False

    def wait_new_link_form_visible(self) -> bool:
        """等待新建表单可见"""
        try:
            self._active_page.locator(self.NEW_LINK_FORM_READY).first.wait_for(
                state="visible",
                timeout=self.NEW_LINK_FORM_WAIT_TIMEOUT_MS,
            )
            return True
        except PlaywrightTimeoutError:
            return False

    def fill_new_link_form(
        self,
        link_name: str,
        button_text: str = "",
        landing_page_name: str = "",
        product_keyword: str = "",
        target_url: str = "https://example.com",
        media_keyword: str = "",
        attribution_tool_keyword: str = "",
        domain_keyword: str = "",
        region_keyword: str = "",
        event_keyword: str = "",
        times_keyword: str = "",
    ) -> str:
        """
        填写新建表单，返回可用于列表校验的标识（优先链接名称）
        """
        identifier = link_name

        # 新页签详情页常见必填：产品、媒体、目标URL、域名、地区、链接名称
        if self._has_visible_input(self.PRODUCT_INPUT_SELECTORS):
            if not self._select_dropdown_with_retry(self.PRODUCT_INPUT_SELECTORS, product_keyword):
                raise AssertionError("未能完成“选择产品”")
            # 选择产品后，页面会动态更新部分下游字段
            self._active_page.wait_for_timeout(600)

        if self._has_visible_input(self.MEDIA_INPUT_SELECTORS):
            self._select_dropdown_with_retry(self.MEDIA_INPUT_SELECTORS, media_keyword)

        # 归因工具（部分产品选择后会出现，通常为必填）
        if self._has_visible_input(self.ATTRIBUTION_TOOL_INPUT_SELECTORS):
            if not self._select_dropdown_with_retry(
                self.ATTRIBUTION_TOOL_INPUT_SELECTORS, attribution_tool_keyword
            ):
                raise AssertionError("未能完成“归因工具”选择")
            if self._has_visible_input(self.ATTRIBUTION_CLICK_URL_INPUT_SELECTORS):
                if not self._fill_first_visible_input(self.ATTRIBUTION_CLICK_URL_INPUT_SELECTORS, target_url):
                    raise AssertionError("未能填写“归因点击URL”")

        if self._has_visible_input(self.DOMAIN_INPUT_SELECTORS):
            if not self._select_dropdown_with_retry(self.DOMAIN_INPUT_SELECTORS, domain_keyword):
                raise AssertionError("未能完成“投放域名”选择")

        if self._has_visible_input(self.REGION_INPUT_SELECTORS):
            if not self._select_dropdown_with_retry(self.REGION_INPUT_SELECTORS, region_keyword):
                raise AssertionError("未能完成“地区分级”选择")

        # 回流落地页是卡片+抽屉选择模式（新建详情页）
        if self._has_visible_locator(self.REFLUX_LANDING_CARD_SELECTORS):
            if not self._select_reflux_landing_page():
                raise AssertionError("未能完成“回流落地页”选择")

        if self._has_visible_input(self.REFLUX_LANDING_SELECTORS):
            if not self._select_dropdown_with_retry(self.REFLUX_LANDING_SELECTORS):
                raise AssertionError("未能完成“回流落地页”选择")

        # 关闭投诉回流开关，可避免事件/次数相关必填项
        self.disable_complaint_backflow_if_enabled()

        if self._has_visible_input(self.EVENT_INPUT_SELECTORS):
            self._select_dropdown_with_retry(self.EVENT_INPUT_SELECTORS, event_keyword)

        if self._has_visible_input(self.TIMES_INPUT_SELECTORS):
            self._select_dropdown_with_retry(self.TIMES_INPUT_SELECTORS, times_keyword)

        if self._has_visible_input(self.TARGET_URL_INPUT_SELECTORS):
            if not self._fill_first_visible_input(self.TARGET_URL_INPUT_SELECTORS, target_url):
                raise AssertionError("未能填写“目标页面URL”")

        # 旧弹窗模式字段：有则填，无则跳过
        if button_text:
            self._fill_first_visible_input(self.BUTTON_TEXT_INPUT_SELECTORS, button_text)

        # 链接名称在基础信息区（页面较靠下），放到后段填写可避免前段字段被折叠
        if not self._fill_first_visible_input(self.LINK_NAME_INPUT_SELECTORS, link_name):
            raise AssertionError("未能填写“链接名称”")

        if landing_page_name and self._fill_first_visible_input(self.LANDING_NAME_INPUT_SELECTORS, landing_page_name):
            if not identifier:
                identifier = landing_page_name

        # 详情页备注字段（可选）
        self._fill_first_visible_input(self.REMARK_INPUT_SELECTORS, f"auto created: {identifier or link_name}")

        return identifier

    def submit_new_link_form(self) -> bool:
        """提交新建表单"""
        return self._click_first_visible(self.SUBMIT_BUTTON_SELECTORS)

    def wait_create_success(self, timeout: int = 10000) -> bool:
        """等待创建成功提示"""
        for selector in self.SUCCESS_MESSAGE_SELECTORS:
            try:
                self._active_page.locator(selector).first.wait_for(state="visible", timeout=timeout)
                return True
            except PlaywrightTimeoutError:
                continue
        return False

    def get_visible_form_errors(self) -> list[str]:
        """获取页面当前可见的表单错误提示文案"""
        return self._active_page.eval_on_selector_all(
            ".arco-form-item-message, .arco-form-item-explain, .arco-message-notice, .arco-notification",
            "els => els.filter(e => !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length)).map(e => (e.textContent||'').trim()).filter(Boolean)"
        )

    def disable_complaint_backflow_if_enabled(self) -> bool:
        """如果“投诉回流设置”开关开启则将其关闭"""
        for _ in range(8):
            for selector in self.COMPLAINT_SWITCH_SELECTORS:
                switch = self._active_page.locator(selector).first
                if switch.count() == 0:
                    continue
                try:
                    switch.scroll_into_view_if_needed(timeout=2000)
                    if not switch.is_visible():
                        continue
                except Exception:
                    continue

                is_checked = self._is_switch_checked(switch)
                if is_checked:
                    switch.click(timeout=self.timeout, force=True)
                    self._active_page.wait_for_timeout(300)
                    # 某些组件 click 事件被遮挡，兜底触发原生点击
                    if self._is_switch_checked(switch):
                        try:
                            switch.evaluate("el => el.click()")
                            self._active_page.wait_for_timeout(300)
                        except Exception:
                            pass
                return True
            self._active_page.mouse.wheel(0, 600)
            self._active_page.wait_for_timeout(200)
        return False

    def search_by_keyword(self, keyword: str):
        """在列表搜索框中输入关键词"""
        locator = self._active_page.locator(self.SEARCH_INPUT).first
        if locator.count() > 0 and locator.is_visible():
            locator.fill(keyword, timeout=self.timeout)
            self._active_page.keyboard.press("Enter")

    def is_list_page(self) -> bool:
        """是否处于可进行列表检索的页面"""
        return (
            self._active_page.locator(self.SEARCH_INPUT).count() > 0
            and self._active_page.locator(self.TABLE_SELECTOR).count() > 0
        )

    def is_keyword_visible_in_table(self, keyword: str, timeout: int = 8000) -> bool:
        """检查表格中是否出现关键词"""
        try:
            table = self._active_page.locator(self.TABLE_SELECTOR).first
            table.locator(f"text={keyword}").first.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def _fill_first_visible_input(self, selectors: list[str], value: str) -> bool:
        for selector in selectors:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                locator = locators.nth(idx)
                try:
                    if locator.is_visible():
                        locator.fill(value, timeout=self.timeout)
                        return True
                except Exception:
                    continue
        return False

    def _has_visible_input(self, selectors: list[str]) -> bool:
        for selector in selectors:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                locator = locators.nth(idx)
                try:
                    if locator.is_visible():
                        return True
                except Exception:
                    continue
        return False

    def _click_first_visible(self, selectors: list[str]) -> bool:
        for selector in selectors:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                locator = locators.nth(idx)
                try:
                    if locator.is_visible():
                        locator.click(timeout=self.timeout)
                        return True
                except Exception:
                    continue
        return False

    def _select_dropdown_first_option(self, selectors: list[str], keyword: str = "") -> bool:
        for selector in selectors:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                locator = locators.nth(idx)
                try:
                    if not locator.is_visible():
                        continue
                    locator.click(timeout=self.timeout)
                except Exception:
                    continue

                self._active_page.wait_for_timeout(250)
                if keyword:
                    try:
                        locator.fill(keyword, timeout=self.timeout)
                    except Exception:
                        pass

                if self._click_first_enabled_regular_option(keyword=keyword):
                    return True

                # 兼容 cascader 场景（产品选择等）
                if self._select_first_cascader_leaf():
                    return True
        return False

    def _has_visible_locator(self, selectors: list[str]) -> bool:
        for selector in selectors:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                locator = locators.nth(idx)
                try:
                    if locator.is_visible():
                        return True
                except Exception:
                    continue
        return False

    def _select_dropdown_with_retry(self, selectors: list[str], keyword: str = "", attempts: int = 3) -> bool:
        for _ in range(attempts):
            if self._select_dropdown_first_option(selectors, keyword):
                return True
            self._active_page.wait_for_timeout(350)
        return False

    def _select_reflux_landing_page(self) -> bool:
        # 1) 点击“请选择回流落地页”卡片，打开抽屉
        clicked = False
        for selector in self.REFLUX_LANDING_CARD_SELECTORS:
            locators = self._active_page.locator(selector)
            for idx in range(locators.count()):
                card = locators.nth(idx)
                try:
                    if not card.is_visible():
                        continue
                    card.scroll_into_view_if_needed(timeout=2000)
                    card.click(timeout=self.timeout)
                    clicked = True
                    break
                except Exception:
                    continue
            if clicked:
                break
        if not clicked:
            return False

        drawer_visible = False
        for selector in self.REFLUX_DRAWER_SELECTORS:
            drawer = self._active_page.locator(selector).first
            if drawer.count() > 0 and drawer.is_visible():
                drawer_visible = True
                break
        if not drawer_visible:
            return False

        # 2) 选中第一条可见模板
        chosen = False
        for _ in range(15):
            for selector in self.REFLUX_DRAWER_ITEM_SELECTORS:
                items = self._active_page.locator(selector)
                if items.count() > 0:
                    items.first.click(timeout=self.timeout)
                    chosen = True
                    break
            if chosen:
                break
            self._active_page.wait_for_timeout(200)
        if not chosen:
            return False

        self._active_page.wait_for_timeout(200)

        # 3) 确认选择
        confirmed = self._click_first_visible(self.REFLUX_DRAWER_CONFIRM_SELECTORS)
        if confirmed:
            self._active_page.wait_for_timeout(300)
        return confirmed

    def _click_first_enabled_regular_option(self, keyword: str = "") -> bool:
        options = self._active_page.locator(
            ".arco-select-option:visible:not(.arco-select-option-disabled):not([aria-disabled='true']), "
            ".arco-dropdown-option:visible:not(.arco-dropdown-option-disabled):not([aria-disabled='true']), "
            "[role='option']:visible:not([aria-disabled='true'])"
        )
        if options.count() == 0:
            return False
        if keyword:
            needle = keyword.strip().lower()
            if needle:
                for idx in range(options.count()):
                    option = options.nth(idx)
                    try:
                        text = option.inner_text().strip().lower()
                    except Exception:
                        continue
                    if needle in text:
                        option.click(timeout=self.timeout)
                        return True
        options.first.click(timeout=self.timeout)
        return True

    def _select_first_cascader_leaf(self) -> bool:
        panels = self._active_page.locator(".arco-cascader-panel:visible")
        try:
            panels.first.wait_for(state="visible", timeout=2500)
        except PlaywrightTimeoutError:
            return False
        panel = panels.first

        first_column = panel.locator(".arco-cascader-panel-column").first
        first_items = first_column.locator(
            "li.arco-cascader-option:not([aria-disabled='true']), "
            "li[role='menuitem']:not([aria-disabled='true'])"
        )
        for _ in range(15):
            if first_items.count() > 0:
                break
            self._active_page.wait_for_timeout(200)
        if first_items.count() == 0:
            return False

        first_items.first.click(timeout=self.timeout)

        # 等待二级列（如存在）渲染完成
        for _ in range(10):
            columns = panel.locator(".arco-cascader-panel-column")
            if columns.count() > 1:
                break
            self._active_page.wait_for_timeout(200)

        columns = panel.locator(".arco-cascader-panel-column")
        if columns.count() > 1:
            last_col = columns.nth(columns.count() - 1)
            leaf_items = last_col.locator(
                "li.arco-cascader-option:not([aria-disabled='true']), "
                "li[role='menuitem']:not([aria-disabled='true'])"
            )
            if leaf_items.count() > 0:
                leaf_items.first.click(timeout=self.timeout)
        return True

    @staticmethod
    def _is_switch_checked(switch_locator) -> bool:
        try:
            return bool(
                switch_locator.evaluate(
                    """el => {
  const aria = el.getAttribute('aria-checked');
  if (aria === 'true') return true;
  if (aria === 'false') return false;
  const cls = el.className || '';
  if (cls.includes('checked')) return true;
  const checkedInput = el.querySelector('input:checked');
  return !!checkedInput;
}"""
                )
            )
        except Exception:
            return False
