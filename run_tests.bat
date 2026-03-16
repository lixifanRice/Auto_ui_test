@echo off
REM 测试运行脚本 (Windows)

echo ==========================================
echo Playwright 自动化测试框架
echo ==========================================

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 安装 Playwright 浏览器
echo 安装 Playwright 浏览器...
playwright install

REM 检查 .env 文件
if not exist ".env" (
    echo 创建 .env 文件...
    copy env.example .env
    echo 请编辑 .env 文件设置你的测试配置
)

REM 运行测试
echo 运行测试...
pytest %*

