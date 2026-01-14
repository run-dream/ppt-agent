import json
from langchain_core.messages import HumanMessage
from src.models.state import PPTState
from src.utils.llm_factory import LLMFactory
from src.utils.prompt_manager import read_prompt
from src.utils.tools import search_real_photo, generate_creative_image
from src.utils.logger import logger

def visual_agent_node(state: PPTState) -> PPTState:
    """
    智能视觉 Agent 节点：自主决定搜索还是生成图片
    """
    slides = state.get("slides", [])
    if not slides:
        return state

    logger.info(f"Visual Agent: Processing {len(slides)} slides with tools...")
    
    # 获取能够调用工具的模型
    llm = LLMFactory.get_model("image_advisor")
    tools = [search_real_photo, generate_creative_image]
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = read_prompt("visual_agent")
    
    updated_slides = slides.copy()
    
    for i, slide in enumerate(updated_slides):
        logger.info(f"Visual Agent: Deciding for Slide {i+1}: {slide.title}")
        
        # 构造单页幻灯片的信息
        slide_info = f"Slide Index: {i+1}\nTitle: {slide.title}\nPoints: {', '.join(slide.bullet_points)}\nSuggested Query: {slide.image_query}"
        
        messages = [
            ("system", system_prompt),
            ("user", f"请为这张幻灯片获取图片：\n{slide_info}")
        ]
        
        try:
            # Agent 决策并执行
            response = llm_with_tools.invoke(messages)
            
            # 处理 Tool Calls
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    args = tool_call["args"]
                    
                    if tool_name == "search_real_photo":
                        result = search_real_photo.invoke(args)
                    elif tool_name == "generate_creative_image":
                        result = generate_creative_image.invoke(args)
                    else:
                        result = ""
                    
                    if result and result.startswith("http"):
                        slide.image_path = result
                        logger.info(f"Visual Agent: Slide {i+1} got image via {tool_name}")
            
        except Exception as e:
            logger.error(f"Visual Agent: Error processing slide {i+1}: {str(e)}")
            
    return {
        **state,
        "slides": updated_slides,
        "current_step": "final_render"
    }
