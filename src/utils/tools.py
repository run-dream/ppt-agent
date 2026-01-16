from langchain_core.tools import tool
from src.utils.unsplash_searcher import UnsplashSearcher
from src.utils.image_searcher import ImageSearcher
from src.utils.image_generator import WanxGenerator
from src.utils.logger import logger

@tool
def search_real_photo(query: str):
    """
    当需要真实的、摄影类的、存在于现实世界中的事物图片时，调用此工具从 Unsplash 中搜索高质量照片。
    参数 query: 英文搜索关键词。
    """
    logger.info(f"Tool Call: search_real_photo('{query}')")
    urls = UnsplashSearcher.search_images(query)
    return urls[0] if urls else "未找到合适的真实照片"

@tool
def generate_creative_image(prompt: str):
    """
    当需要创意插画、科幻场景、抽象概念或搜索引擎难以找到合适图片时，调用此工具使用 AI 生成图片。
    参数 prompt: 详细的视觉描述词（英文）。
    """
    logger.info(f"Tool Call: generate_creative_image('{prompt}')")
    url = WanxGenerator.generate_image(prompt)
    return url if url else "AI 图像生成失败"
