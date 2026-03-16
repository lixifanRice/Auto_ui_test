# Playwright 自动化测试框架

这是一个基于 Playwright 和 pytest 的自动化测试框架，采用页面对象模型（Page Object Model）设计模式。

## 项目结构

```
playwright_learn/
├── pages/              # 页面对象模型
│   ├── __init__.py
│   ├── base_page.py    # 基础页面类
│   └── home_page.py    # 示例页面对象
├── tests/              # 测试用例
│   ├── __init__.py
│   └── test_example.py # 示例测试用例
├── utils/              # 工具类
│   ├── __init__.py
│   ├── config.py       # 配置管理
│   ├── logger.py       # 日志工具
│   └── helpers.py      # 辅助函数
├── reports/            # 测试报告（自动生成）
├── screenshots/        # 截图（自动生成）
├── logs/               # 日志文件（自动生成）
├── conftest.py         # pytest 配置文件
├── pytest.ini          # pytest 配置
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```

## 安装步骤

### 1. 安装 Python 依赖

```bash
# 激活虚拟环境（如果使用虚拟环境）
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置你的测试环境配置：

```env
BASE_URL=https://your-test-site.com
HEADLESS=True
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
```

## 使用方法

### 运行所有测试

```bash
pytest
```

### 运行指定标记的测试

```bash
# 运行冒烟测试
pytest -m smoke

# 运行回归测试
pytest -m regression

# 运行登录相关测试
pytest -m login
```

### 运行指定测试文件

```bash
pytest tests/test_example.py
```

### 运行指定测试用例

```bash
pytest tests/test_example.py::test_example_basic
```

### 并行运行测试

```bash
pytest -n auto
```

### 生成 HTML 报告

```bash
pytest --html=reports/report.html --self-contained-html
```

### 调试模式（非无头模式）

在 `.env` 文件中设置 `HEADLESS=False`，或运行时指定：

```bash
HEADLESS=False pytest
```

## 编写测试用例

### 1. 创建页面对象

在 `pages/` 目录下创建页面对象类，继承 `BasePage`：

```python
from pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

### 2. 编写测试用例

在 `tests/` 目录下创建测试文件：

```python
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.mark.login
def test_user_login(page: Page):
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.login("username", "password")
    assert "dashboard" in page.url
```

## 测试标记

框架支持以下测试标记：

- `@pytest.mark.smoke` - 冒烟测试
- `@pytest.mark.regression` - 回归测试
- `@pytest.mark.login` - 登录相关测试
- `@pytest.mark.api` - API测试

## 配置说明

### pytest.ini

pytest 配置文件，包含测试发现规则、标记定义等。

### conftest.py

pytest 配置文件，包含全局 fixtures：
- `browser` - 浏览器实例
- `page` - 页面实例
- `base_url` - 基础URL
- 自动截图功能（测试失败时）

### utils/config.py

配置管理类，统一管理所有配置项。

## 最佳实践

1. **使用页面对象模型**：将页面元素和操作封装在页面对象中
2. **使用标记分类测试**：使用 pytest 标记对测试进行分类
3. **合理使用等待**：使用框架提供的等待方法，避免硬编码 sleep
4. **错误处理**：测试失败时自动截图，便于调试
5. **日志记录**：使用 logger 记录关键操作和错误信息
6. **环境隔离**：使用 `.env` 文件管理不同环境的配置

## 报告和日志

- **HTML 报告**：运行测试后，在 `reports/report.html` 查看测试报告
- **截图**：测试失败时，截图保存在 `reports/screenshots/`
- **日志**：日志文件保存在 `logs/` 目录，按日期命名

## 常见问题

### Q: 如何切换浏览器？

A: 在 `conftest.py` 中修改 `browser_type_launch_args` fixture，或使用 pytest 参数：

```bash
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

### Q: 如何设置超时时间？

A: 在 `.env` 文件中设置 `BROWSER_TIMEOUT` 和 `DEFAULT_TIMEOUT`。

### Q: 如何调试测试？

A: 设置 `HEADLESS=False` 可以看到浏览器操作，或使用 `pytest --pdb` 进入调试模式。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
