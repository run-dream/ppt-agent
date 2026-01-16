#!/usr/bin/env python3
"""
ChatPPT 主入口脚本

运行方式：
    python main.py ui      # 启动 Web UI
    python main.py test    # 运行命令行测试
"""

import sys
import os

# 添加 src 目录到 Python 路径
project_root = os.path.dirname(__file__)
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 初始化 LangSmith (如果配置了)
from dotenv import load_dotenv
load_dotenv()

# 启用 LangSmith tracing（如果配置了相关环境变量）
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
langsmith_endpoint = os.getenv("LANGSMITH_ENDPOINT")
langsmith_project = os.getenv("LANGSMITH_PROJECT")

if langsmith_api_key and langsmith_project:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
    if langsmith_endpoint:
        os.environ["LANGCHAIN_ENDPOINT"] = langsmith_endpoint
    os.environ["LANGCHAIN_PROJECT"] = langsmith_project

    print(f"🔍 LangSmith tracing 已启用 (项目: {langsmith_project})")
else:
    print("🔍 LangSmith tracing 未启用 (未配置相关环境变量)")

def main():
    if len(sys.argv) < 2:
        print("用法: python main.py [ui|test]")
        print("  ui   - 启动 Web UI")
        print("  test - 运行命令行测试")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "ui":
        print("🚀 启动 ChatPPT Web UI...")
        from ui.gradio_app import create_ui
        import gradio as gr

        demo = create_ui()
        # 修复 Gradio 6.0 API 变更
        # 禁用代理对 localhost 的影响
        os.environ['no_proxy'] = '127.0.0.1,localhost'

        demo.launch(
            theme=gr.themes.Soft(),
            server_name="0.0.0.0",  # 绑定到所有接口
            server_port=7861,  # 换个端口
            show_error=True,
            share=False,
            enable_monitoring=False,
            # 绕过代理设置
            app_kwargs={
                "timeout": 120,
                "proxy_headers": False
            }
        )

    elif command == "test":
        print("🧪 运行 ChatPPT 简单测试...")

        # 简单的环境检查测试
        print("✅ Python 环境正常")

        try:
            import gradio as gr
            print(f"✅ Gradio {gr.__version__} 已安装")
        except ImportError as e:
            print(f"❌ Gradio 未安装: {e}")
            print("   💡 运行: pip install gradio")

        try:
            from dotenv import load_dotenv
            print("✅ python-dotenv 已安装")
        except ImportError:
            print("❌ python-dotenv 未安装")

        try:
            import langchain
            print(f"✅ LangChain {langchain.__version__} 已安装")
        except ImportError:
            print("❌ LangChain 未安装")

        print("\n🎯 环境检查完成！")
        print("💡 如果要运行完整测试，请配置 .env 文件中的 API Key，然后使用:")
        print("   python -m src.ui.gradio_app  # 或 python main.py ui")

    else:
        print(f"未知命令: {command}")
        print("可用命令: ui, test")
        sys.exit(1)

if __name__ == "__main__":
    main()