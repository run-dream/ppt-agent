import os
import requests
from src.utils.logger import logger

class WanxGenerator:
    """
    阿里云通义万相图像生成工具
    """
    
    @staticmethod
    def generate_image(prompt: str) -> str:
        """
        调用通义万相生成图片并返回 URL
        """
        api_key = os.getenv("LLM_API_KEY")
        model = os.getenv("IMAGE_GEN_MODEL", "wanx-v1")
        
        logger.info(f"Wanx: Generating image for prompt: {prompt[:50]}...")
        
        try:
            rsp = dashscope.ImageSynthesis.call(
                api_key=api_key,
                model=model,
                prompt=prompt,
                n=1,
                size='1024*1024'
            )
            
            if rsp.status_code == 200:
                image_url = rsp.output.results[0].url
                logger.info(f"Wanx: Image generated successfully: {image_url}")
                return image_url
            else:
                logger.error(f"Wanx: Failed to generate image. Code: {rsp.code}, Message: {rsp.message}")
                return ""
        except Exception as e:
            logger.exception("Wanx: Exception during image generation")
            return ""
