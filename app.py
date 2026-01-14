import os
from dotenv import load_dotenv
from src.workflow.graph import app
from src.utils.logger import logger

load_dotenv()

def main():
    logger.info("--- ChatPPT Workflow Test ---")
    
    # 模拟用户输入
    user_input = "请帮我制作一个关于'人工智能在医疗领域应用'的 PPT，包含现状、挑战和未来趋势。"
    
    # 初始化状态
    initial_state = {
        "input_text": user_input,
        "input_files": [],
        "outline": None,
        "slides": [],
        "current_step": "start",
        "is_approved": False,
        "error": None
    }
    
    # 运行工作流
    logger.info(f"User Input: {user_input}")
    logger.info("Running workflow (Planner -> Generator)...")
    
    result = app.invoke(initial_state)
    
    if result.get("error"):
        logger.error(f"Error: {result['error']}")
    else:
        # 打印大纲
        outline = result.get("outline")
        if outline:
            logger.info("--- Generated PPT Outline ---")
            logger.info(f"Title: {outline.title}")
            for i, chapter in enumerate(outline.chapters, 1):
                logger.info(f"  {i}. {chapter}")
        
        # 打印幻灯片内容
        slides = result.get("slides", [])
        if slides:
            logger.info("--- Generated Slides Content ---")
            for i, slide in enumerate(slides, 1):
                logger.info(f"Slide {i}: {slide.title}")
                for point in slide.bullet_points:
                    logger.info(f"  - {point}")
                logger.info(f"  Image Query: {slide.image_query}")
                logger.info(f"  Layout: {slide.layout_type}")
                logger.info("-" * 20)
        else:
            logger.warning("No slides content generated.")

if __name__ == "__main__":
    main()
