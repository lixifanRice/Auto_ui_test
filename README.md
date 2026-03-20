# Auto UI Test (Playwright + pytest)

基于 `pytest + playwright` 的 UI 自动化项目，当前已落地「回流链接创建」主流程测试，采用 POM（页面对象）组织方式。

## 项目现状

- 运行框架：`pytest` + `pytest-playwright`
- 默认浏览器：`chromium` + `chrome channel`（见 `pytest.ini`）
- 认证方式：`conftest.py` 中自动注入
  - `CF_Authorization` Cookie
  - `AUTH_BEARER` 请求头
- 当前核心业务用例：`tests/promotion_management/test_backflow_link.py::test_create_backflow_link`

## 目录结构

```text
Auto_ui_test/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── env.example
├── run_tests.sh
├── run_tests.bat
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   └── promotional_link_page.py
├── tests/
│   ├── __init__.py
│   ├── promotion_management/
│   │   ├── test_backflow_link.py
│   │   ├── test_product_library.py
│   │   └── test_domain.py
│   ├── backflow_features/
│   │   ├── test_backflow_landing_page.py
│   │   ├── test_audience_backflow.py
│   │   ├── test_smart_shield.py
│   │   ├── test_complaint_backflow.py
│   │   ├── test_pwa_backflow.py
│   │   ├── test_push_backflow.py
│   │   └── test_returning_user_landing_page.py
│   └── finance/
│       └── test_wallet.py
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── helpers.py
├── test_data/
├── logs/
└── reports/
```

## 环境要求

- Python `3.9+`
- 推荐使用项目内虚拟环境 `venv`

## 安装

1. 创建并激活虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bat
python -m venv venv
venv\Scripts\activate
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 安装 Playwright 浏览器

```bash
playwright install
```

## 配置 `.env`

复制示例文件：

```bash
cp env.example .env
```

最少需要确认这些项：

- `BASE_URL`
- `HEADLESS`
- `BROWSER_TIMEOUT`
- `VIEWPORT_WIDTH` / `VIEWPORT_HEIGHT`

若目标环境有登录/CF 校验，需要配置：

- `CF_Authorization`
- `AUTH_BEARER`

业务用例可选参数（不填则自动选首项）：

- `PROMO_PRODUCT_KEYWORD`
- `PROMO_MEDIA_KEYWORD`
- `PROMO_ATTRIBUTION_TOOL_KEYWORD`
- `PROMO_DOMAIN_KEYWORD`
- `PROMO_REGION_KEYWORD`
- `PROMO_EVENT_KEYWORD`
- `PROMO_TIMES_KEYWORD`
- `PROMO_TARGET_URL`

## 模块划分（对应左侧菜单）

- `promotion_management`（推广管理）
  - `backflow_link`（回流链接）
  - `product_library`（产品库）
  - `domain`（域名）
- `backflow_features`（回流功能）
  - `backflow_landing_page`（回流落地页）
  - `audience_backflow`（受众回流）
  - `smart_shield`（智能绿盾）
  - `complaint_backflow`（投诉回流）
  - `pwa_backflow`（PWA回流）
  - `push_backflow`（推送回流）
  - `returning_user_landing_page`（老客落地页）
- `finance`（财务）
  - `wallet`（钱包）

说明：除 `backflow_link` 外，其他菜单项当前为占位用例（`skip`），用于先完成模块分层。

## 运行测试

说明：如果你本机没有全局 `pytest`，请用 `./venv/bin/python -m pytest`。

运行全部用例：

```bash
./venv/bin/python -m pytest
```

运行“推广管理”模块：

```bash
./venv/bin/python -m pytest tests/promotion_management
```

运行单条核心用例：

```bash
./venv/bin/python -m pytest tests/promotion_management/test_backflow_link.py::test_create_backflow_link -vv -s
```

按标记运行：

```bash
./venv/bin/python -m pytest -m smoke
./venv/bin/python -m pytest -m regression
./venv/bin/python -m pytest -m promotion_management
./venv/bin/python -m pytest -m backflow_features
./venv/bin/python -m pytest -m finance
```

并行运行：

```bash
./venv/bin/python -m pytest -n auto
```

## 默认运行配置（来自 `pytest.ini`）

- `--browser=chromium`
- `--browser-channel=chrome`
- 自动生成 HTML 报告：
  - `reports/report.html`

因此通常不需要每次额外传浏览器参数。

## 报告与产物

- HTML 报告：`reports/report.html`
- 失败截图：`reports/screenshots/`
- 日志文件：`logs/test_YYYYMMDD.log`
- 可选视频（开启 `RECORD_VIDEO=True`）：`reports/videos/`

## 关键实现说明

- `conftest.py`
  - 统一创建 browser context
  - 注入认证信息（Cookie/Header）
  - 失败自动截图
- `pages/promotional_link_page.py`
  - 封装“新建回流链接”流程
  - 兼容新页签打开
  - 处理动态表单、抽屉选择、投诉回流开关
- `tests/promotion_management/test_backflow_link.py`
  - 核心业务测试入口

## 常见问题

1. 命令找不到 `pytest`

使用：

```bash
./venv/bin/python -m pytest
```

2. 进入 Cloudflare 登录页

检查 `.env` 中：

- `CF_Authorization`
- `AUTH_BEARER`
- `BASE_URL` 域名是否匹配

3. 页面可见但用例失败

- 先看 `reports/report.html`
- 再看 `reports/screenshots/` 失败截图和 `logs/` 日志

## 安全建议

- 不要在仓库提交真实的 `CF_Authorization`、`AUTH_BEARER`、账号密码。
- 建议将 `env.example` 保持为占位符示例值，仅在本地 `.env` 使用真实凭证。
