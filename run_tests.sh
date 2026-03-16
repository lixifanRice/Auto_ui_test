#!/bin/bash
# 测试运行脚本

echo "=========================================="
echo "Playwright 自动化测试框架"
echo "=========================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 安装 Playwright 浏览器
echo "安装 Playwright 浏览器..."
playwright install

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件..."
    cp env.example .env
    echo "请编辑 .env 文件设置你的测试配置"
fi

# 运行测试
echo "运行测试..."
pytest "$@"

