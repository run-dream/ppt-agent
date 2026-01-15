#!/usr/bin/env python3
"""
网络配置调试脚本
检查可能影响 Gradio 运行的网络配置
"""

import os
import sys
import socket

def check_network():
    print("🔍 检查网络配置...")

    # 检查环境变量
    print("\n📋 环境变量检查:")
    proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'no_proxy', 'NO_PROXY']
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ⚠️  {var} = {value}")

    # 检查端口占用
    print("\n🔌 端口检查:")
    ports_to_check = [7860, 7861, 7862]
    for port in ports_to_check:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                print(f"  ❌ 端口 {port} 被占用")
            else:
                print(f"  ✅ 端口 {port} 可用")
        except Exception as e:
            print(f"  ❓ 端口 {port} 检查失败: {e}")

    # 检查 localhost 解析
    print("\n🌐 本地主机检查:")
    try:
        localhost_ip = socket.gethostbyname('localhost')
        print(f"  ✅ localhost 解析为: {localhost_ip}")
    except Exception as e:
        print(f"  ❌ localhost 解析失败: {e}")

    # 测试本地连接
    print("\n🔗 本地连接测试:")
    try:
        import requests
        # 尝试连接到一个不存在的本地端口，应该快速失败
        try:
            requests.get('http://127.0.0.1:7860', timeout=1)
            print("  ⚠️  端口 7860 有响应（可能被其他服务占用）")
        except requests.exceptions.ConnectionError:
            print("  ✅ 端口 7860 无响应（正常）")
        except Exception as e:
            print(f"  ❓ 连接测试异常: {e}")
    except ImportError:
        print("  ⚠️  requests 未安装，无法进行连接测试")

    print("\n🎯 调试完成！")
    print("💡 如果仍有问题，尝试：")
    print("   1. 关闭其他可能占用端口的应用")
    print("   2. 临时禁用代理设置")
    print("   3. 使用不同的端口")

if __name__ == "__main__":
    check_network()