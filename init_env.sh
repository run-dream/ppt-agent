#!/bin/bash
# ChatPPT 环境初始化脚本

set -e

echo "🚀 ChatPPT 环境初始化开始..."

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ 检测到 Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "⚠️  虚拟环境已存在，跳过创建"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装项目依赖..."
pip install -r requirements.txt

echo ""
echo "✨ 环境初始化完成！"
echo ""
echo "📝 使用说明:"
echo "   1. 激活环境: source venv/bin/activate"
echo "   2. 配置 .env: cp env.example .env 并填写 API Key"
echo "   3. 启动 UI: python src/ui/gradio_app.py"
echo ""
