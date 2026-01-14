from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.models.state import PPTState, SlideContent
from src.utils.llm_factory import LLMFactory
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
        ("user", "PPT 总标题: {title}\n大纲章节: {chapters}\n请根据大纲生成每一页幻灯片的具体内容。")
    ])
    
    # 使用结构化输出生成列表
    structured_llm = llm.with_structured_output(SlidesList)
    chain = prompt | structured_llm
    
    try:
        chapters_str = ", ".join(outline.chapters)
        result = chain.invoke({
            "title": outline.title,
            "chapters": chapters_str
        })
        
        logger.info(f"Content Generator: Successfully generated {len(result.slides)} slides.")
        return {
            **state,
            "slides": result.slides,
            "current_step": "image_advisory"
        }
    except Exception as e:
        logger.exception("Content Generator: Failed to generate slides.")
        return {
            **state,
            "error": f"Error in content generator: {str(e)}"
        }
