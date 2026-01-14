from langchain_core.prompts import ChatPromptTemplate
from src.models.state import PPTState, PPTOutline
from src.utils.llm_factory import LLMFactory
from src.utils.prompt_manager import read_prompt
from src.utils.logger import logger

def content_planner_node(state: PPTState) -> PPTState:
    """
    大纲生成节点：根据用户输入生成 PPT 大纲
    """
    input_text = state.get("input_text", "")
    if not input_text:
        logger.error("Content Planner: No input text provided.")
        return {**state, "error": "No input text provided"}

    logger.info(f"Content Planner: Generating outline for: {input_text[:50]}...")
    
    # 获取 planner 专用的模型
    llm = LLMFactory.get_model("planner")
    
    # 从外部文件读取按照 RoleTaskFormat 编写的 Prompts
    system_prompt = read_prompt("planner")
    
    # 定义提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    
    # 使用结构化输出
    structured_llm = llm.with_structured_output(PPTOutline)
    chain = prompt | structured_llm
    
    try:
        outline = chain.invoke({"input": input_text})
        logger.info(f"Content Planner: Successfully generated outline: {outline.title}")
        return {
            **state,
            "outline": outline,
            "current_step": "content_generation"
        }
    except Exception as e:
        logger.exception("Content Planner: Failed to generate outline.")
        return {
            **state,
            "error": f"Error in content planner: {str(e)}"
        }
