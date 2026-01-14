from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from src.models.state import PPTState, SlideContent
from src.utils.llm_factory import LLMFactory
from src.utils.prompt_manager import read_prompt
from src.utils.logger import logger

class ImageQueryRefinement(BaseModel):
    """单个幻灯片的配图优化建议"""
    index: int = Field(description="幻灯片索引")
    refined_query: str = Field(description="优化后的英文搜索关键词")

class ImageAdvisorOutput(BaseModel):
    """配图建议节点的结构化输出"""
    refinements: List[ImageQueryRefinement] = Field(description="针对各张幻灯片的优化列表")

def image_advisor_node(state: PPTState) -> PPTState:
    """
    配图建议节点：优化每张幻灯片的配图关键词，并准备进行搜索
    """
    slides = state.get("slides", [])
    if not slides:
        logger.warning("Image Advisor: No slides found to advise.")
        return state

    logger.info(f"Image Advisor: Refining image queries for {len(slides)} slides...")
    
    # 获取 image_advisor 专用的模型 (qwen-turbo)
    llm = LLMFactory.get_model("image_advisor")
    
    # 从外部文件读取 Prompts
    system_prompt = read_prompt("image_advisor")
    
    # 构造输入内容
    slides_info = "\n".join([
        f"Slide {i+1}: {slide.title}\nPoints: {', '.join(slide.bullet_points)}\nCurrent Query: {slide.image_query}"
        for i, slide in enumerate(slides)
    ])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", f"以下是 PPT 的幻灯片内容，请为每张幻灯片提供一个优化的英文图像搜索关键词：\n\n{slides_info}")
    ])
    
    # 使用结构化输出
    structured_llm = llm.with_structured_output(ImageAdvisorOutput)
    chain = prompt | structured_llm
    
    try:
        result = chain.invoke({})
        
        # 更新 state 中的 slides
        updated_slides = slides.copy()
        for refinement in result.refinements:
            idx = refinement.index - 1
            if 0 <= idx < len(updated_slides):
                updated_slides[idx].image_query = refinement.refined_query
                logger.info(f"Slide {refinement.index} query refined: {refinement.refined_query}")
        
        return {
            **state,
            "slides": updated_slides,
            "current_step": "image_searching"
        }
    except Exception as e:
        logger.exception("Image Advisor: Failed to refine queries.")
        return {
            **state,
            "error": f"Error in image advisor: {str(e)}"
        }
