import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMFactory:
    """
    模型工厂：通过 OpenAI 兼容协议连接 LLM 服务 (支持阿里云、DeepSeek 等)
    """
    
    @staticmethod
    def get_model(node_name: str):
        """
        根据节点名称获取对应的模型
        :param node_name: planner, generator, or image_advisor
        """
        api_key = os.getenv("LLM_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        api_base = os.getenv("LLM_API_BASE") or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        
        # 映射不同节点的模型名称
        model_configs = {
            "planner": os.getenv("PLANNER_MODEL", "qwen-max"),
            "generator": os.getenv("GENERATOR_MODEL", "qwen-plus"),
            "image_advisor": os.getenv("IMAGE_ADVISOR_MODEL", "qwen-turbo")
        }
        
        model_name = model_configs.get(node_name, "qwen-plus")
        
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=api_base,
            temperature=0.7
        )
