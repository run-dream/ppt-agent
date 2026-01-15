#!/bin/bash
# 临时禁用代理启动 ChatPPT

echo "🚀 启动 ChatPPT (绕过代理设置)..."

# 备份当前的代理设置
OLD_HTTP_PROXY=$HTTP_PROXY
OLD_HTTPS_PROXY=$HTTPS_PROXY
OLD_NO_PROXY=$NO_PROXY

# 临时禁用代理
unset HTTP_PROXY
unset HTTPS_PROXY
export NO_PROXY="127.0.0.1,localhost"

echo "📋 已临时禁用代理设置"

# 启动应用
python main.py ui

# 恢复代理设置 (如果脚本被中断)
export HTTP_PROXY=$OLD_HTTP_PROXY
export HTTPS_PROXY=$OLD_HTTPS_PROXY
export NO_PROXY=$OLD_NO_PROXY

echo "📋 已恢复代理设置"