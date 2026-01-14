import os
import requests
from src.utils.logger import logger
from typing import List, Optional

class ImageSearcher:
    """
    图像搜索工具类，支持 Bing Image Search 或通过简单爬虫获取图片链接
    """
    
    @staticmethod
    def search_images(query: str, count: int = 1) -> List[str]:
        """
        搜索图片并返回链接列表
        """
        api_key = os.getenv("BING_SEARCH_API_KEY")
        if api_key and api_key != "your_bing_api_key_here":
            return ImageSearcher._search_bing(query, api_key, count)
        else:
            logger.warning(f"Bing API Key not configured. Using placeholder for query: {query}")
            # 返回占位图或通过其他免费方案
            return [f"https://placehold.co/600x400?text={query.replace(' ', '+')}"]

    @staticmethod
    def _search_bing(query: str, api_key: str, count: int) -> List[str]:
        """使用 Bing Image Search API"""
        endpoint = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {"q": query, "count": count, "imageType": "Photo", "safeSearch": "Strict"}
        
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            search_results = response.json()
            return [img["contentUrl"] for img in search_results.get("value", [])[:count]]
        except Exception as e:
            logger.error(f"Bing search failed for '{query}': {str(e)}")
            return []

def image_search_node(state: dict) -> dict:
    """
    图像搜索节点：为每张幻灯片实际检索图片链接
    """
    slides = state.get("slides", [])
    if not slides:
        return state

    logger.info(f"Image Search Node: Searching images for {len(slides)} slides...")
    
    updated_slides = []
    for slide in slides:
        if slide.image_query:
            image_urls = ImageSearcher.search_images(slide.image_query)
            if image_urls:
                # 将第一个结果存入 image_path (目前存链接，后续可以下载到本地)
                slide.image_path = image_urls[0]
                logger.info(f"Image found for '{slide.title}': {slide.image_path}")
        updated_slides.append(slide)
        
    return {
        **state,
        "slides": updated_slides,
        "current_step": "final_render"
    }
