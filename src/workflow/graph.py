from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.models.state import PPTState
from src.nodes.planner import content_planner_node
from src.nodes.generator import content_generator_node
from src.nodes.image_advisor import image_advisor_node
from src.nodes.visual_agent import visual_agent_node
from src.utils.ppt_generator import ppt_generator_node

def create_workflow():
    """创建并编译具有智能 Agent 工具能力的 LangGraph 工作流"""
    
    checkpointer = MemorySaver()
    workflow = StateGraph(PPTState)
    
    # 添加节点
    workflow.add_node("planner", content_planner_node)
    workflow.add_node("generator", content_generator_node)
    workflow.add_node("image_advisor", image_advisor_node)
    workflow.add_node("visual_agent", visual_agent_node)
    workflow.add_node("renderer", ppt_generator_node)
    
    # 设置入口
    workflow.set_entry_point("planner")
    
    # 添加边 (image_searcher 被升级后的 visual_agent 替代)
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "image_advisor")
    workflow.add_edge("image_advisor", "visual_agent")
    workflow.add_edge("visual_agent", "renderer")
    workflow.add_edge("renderer", END)
    
    # 编译
    app = workflow.compile(
        checkpointer=checkpointer,
        interrupt_after=["planner", "image_advisor"]
    )
    return app

# 导出编译好的应用实例
app = create_workflow()
