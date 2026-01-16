import os
import requests
from src.utils.logger import logger

class UnsplashSearcher:
    """
    Unsplash API 图片搜索工具 - 完全免费，无需 API Key
    """

    BASE_URL = "https://api.unsplash.com"
    DEFAULT_CLIENT_ID = "your_unsplash_access_key_here"  # 默认公开的 Access Key

    @staticmethod
    def search_images(query: str, count: int = 1) -> list[str]:
        """
        使用 Unsplash API 搜索图片
        注意：需要有效的 UNSPLASH_ACCESS_KEY 环境变量
        获取方法：https://unsplash.com/developers
        """
        access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        secret_key = os.getenv("UNSPLASH_SECRET_KEY")

        # 检查是否有有效的 Access Key
        if not access_key or access_key == UnsplashSearcher.DEFAULT_CLIENT_ID:
            logger.warning("Unsplash: No valid access key found. Set UNSPLASH_ACCESS_KEY environment variable.")
            logger.warning("Get your key at: https://unsplash.com/developers")
            return []

        params = {
            "query": query,
            "per_page": count,
            "orientation": "landscape",  # 适合 PPT 的横向图片
            "content_filter": "high"     # 只返回高质量图片
        }

        headers = {"Authorization": f"Client-ID {access_key}"}

        # 如果提供了 Secret Key，使用 Bearer Token 认证（更高权限）
        if secret_key:
            # 对于 Confidential Applications，需要先获取 Bearer Token
            # 这里简化为直接使用 Access Key，实际项目中可以扩展为 OAuth 流程
            headers = {"Authorization": f"Bearer {secret_key}"}
            logger.debug("Using Unsplash Bearer Token authentication")

        try:
            response = requests.get(
                f"{UnsplashSearcher.BASE_URL}/search/photos",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            photos = data.get("results", [])

            if not photos:
                logger.warning(f"Unsplash: No results found for '{query}'")
                return []

            # 返回图片的 regular 尺寸 URL（适合 PPT 使用）
            urls = [photo["urls"]["regular"] for photo in photos[:count]]
            logger.info(f"Unsplash: Found {len(urls)} images for '{query}' (auth: {'Bearer' if secret_key else 'Client-ID'})")
            return urls

        except Exception as e:
            logger.error(f"Unsplash search failed for '{query}': {str(e)}")
            return []
