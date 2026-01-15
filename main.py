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
        demo.launch(
            theme=gr.themes.Soft(),
            server_name="127.0.0.1",
            server_port=7860,
            show_error=True
        )

    elif command == "test":
        print("🧪 运行 ChatPPT 简单测试...")

        # 简单的环境检查测试
        print("✅ Python 环境正常")

        try:
            import gradio as gr
            print(f"✅ Gradio {gr.__version__} 已安装")
        except ImportError:
            print("❌ Gradio 未安装")

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