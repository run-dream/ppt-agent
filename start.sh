#!/bin/bash
# ChatPPT 快速启动脚本

set -e

echo "🚀 ChatPPT 快速启动..."

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  建议先激活虚拟环境："
    echo "   source venv/bin/activate"
    echo ""
    echo "继续运行可能会有问题..."
    read -p "是否继续？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，正在从模板创建..."
    cp env.example .env
    echo "✅ 已创建 .env 文件，请编辑其中的 API Key"
    echo ""
fi

# 启动 UI
echo "🌐 启动 ChatPPT Web UI..."
python main.py ui