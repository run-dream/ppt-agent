import os
import requests
from src.utils.logger import logger
from src.utils.unsplash_searcher import UnsplashSearcher
from typing import List, Optional

class ImageSearcher:
    """
    图像搜索工具类，支持多种图片搜索服务：
    1. Unsplash API (免费，无速率限制)
    2. Bing Image Search (需要 API Key)
    3. 占位图 (fallback)
    """

    @staticmethod
    def search_images(query: str, count: int = 1) -> List[str]:
        """
        搜索图片并返回链接列表，可配置是否使用搜索引擎
        """
        # 检查是否启用搜索引擎
        enable_search_engines = os.getenv("ENABLE_IMAGE_SEARCH_ENGINES", "true").lower() == "true"

        if enable_search_engines:
            # 优先使用 Unsplash（完全免费）
            unsplash_results = UnsplashSearcher.search_images(query, count)
            if unsplash_results:
                logger.info(f"ImageSearcher: Using Unsplash results for '{query}'")
                return unsplash_results

            # 如果 Unsplash 失败，尝试 Bing
            api_key = os.getenv("BING_SEARCH_API_KEY")
            if api_key and api_key != "your_bing_api_key_here":
                bing_results = ImageSearcher._search_bing(query, api_key, count)
                if bing_results:
                    logger.info(f"ImageSearcher: Using Bing results for '{query}'")
                    return bing_results

        # 如果禁用搜索引擎或所有搜索服务都失败，使用占位图
        logger.info(f"Image search completed. Using placeholder for '{query}'")
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
