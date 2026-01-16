from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.models.state import PPTState, SlideContent
from src.utils.llm_factory import LLMFactory
from src.utils.layout_manager import LayoutManager
from src.utils.prompt_manager import read_prompt
from src.utils.logger import logger

class SlidesList(BaseModel):
    """用于结构化输出多张幻灯片的列表"""
    slides: List[SlideContent] = Field(description="幻灯片内容列表")

def content_generator_node(state: PPTState) -> PPTState:
    """
    内容生成节点：根据大纲扩写每张幻灯片的详细内容
    """
    outline = state.get("outline")
    if not outline:
        logger.error("Content Generator: No outline found to generate content.")
        return {**state, "error": "No outline found to generate content"}

    logger.info(f"Content Generator: Generating slides for: {outline.title}...")
    
    # 获取 generator 专用的模型 (qwen-plus)
    llm = LLMFactory.get_model("generator")
    
    # 从外部文件读取 Prompts
    system_prompt = read_prompt("generator")
    
    # 定义提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "PPT 总标题: {title}\n大纲章节: {chapters}\n\n请为每个章节生成一张幻灯片，为每一张幻灯片创建合适的标题、要点内容、图片关键词和版式类型。确保每张幻灯片都有非空的标题。")
    ])
    
    # 使用结构化输出生成列表
    structured_llm = llm.with_structured_output(SlidesList)
    chain = prompt | structured_llm
    
    try:
        chapters_str = ", ".join(outline.chapters)
        logger.info(f"Content Generator: Processing outline '{outline.title}' with chapters: {chapters_str}")

        result = chain.invoke({
            "title": outline.title,
            "chapters": chapters_str
        })

        logger.info(f"Content Generator: Successfully generated {len(result.slides)} slides.")

        # 检查并修复生成的slides
        fixed_slides = []
        for i, slide in enumerate(result.slides):
            # 记录原始slide对象的详细信息
            logger.info(f"Content Generator: Slide {i+1} raw data - title: '{slide.title}', layout_type: '{slide.layout_type}', image_query: '{slide.image_query}'")

            # 特殊处理第一张slide（标题页）
            if i == 0:
                # 确保第一张是标题页
                slide.layout_type = "title_slide"
                # 标题页通常不需要图片，清空image_query
                slide.image_query = None
                logger.info(f"Content Generator: Set slide 1 as title slide with layout 'title_slide'")
                fixed_slides.append(slide)
                continue

            # 修复标题
            if not slide.title or slide.title.strip() == "":
                # 对于内容页，如果标题为空，使用对应的章节名
                chapter_index = i - 1  # 因为第一张是标题页，所以章节索引要减1
                if chapter_index < len(outline.chapters):
                    slide.title = outline.chapters[chapter_index]
                    logger.warning(f"Content Generator: Fixed empty title for slide {i+1} to chapter: '{slide.title}'")
                else:
                    slide.title = f"幻灯片 {i+1}"
                    logger.warning(f"Content Generator: Used default title for slide {i+1}: '{slide.title}'")

            # 检查和修复layout_type
            valid_layouts = ["title_slide", "title_content", "section_header", "two_column", "comparison", "title_only", "blank", "content_caption", "picture_caption", "default"]
            if not slide.layout_type or slide.layout_type not in valid_layouts:
                logger.warning(f"Content Generator: Invalid layout_type '{slide.layout_type}' for slide {i+1}, using 'title_content'")
                slide.layout_type = "title_content"  # 默认使用有图片的标准布局
            else:
                logger.info(f"Content Generator: Slide {i+1} layout_type: '{slide.layout_type}' -> layout index: {LayoutManager.get_layout_index(slide.layout_type)}")

            # 检查图片需求：只有特定布局才需要图片
            layouts_with_pictures = ["title_content", "picture_caption"]  # 有图片占位符的布局
            if slide.layout_type not in layouts_with_pictures:
                slide.image_query = None  # 清空不需要图片的布局的image_query
                logger.info(f"Content Generator: Cleared image_query for layout '{slide.layout_type}' (no picture placeholder)")

            fixed_slides.append(slide)

        return {
            **state,
            "slides": fixed_slides,
            "current_step": "image_advisory"
        }
    except Exception as e:
        logger.exception("Content Generator: Failed to generate slides.")
        return {
            **state,
            "error": f"Error in content generator: {str(e)}"
        }
