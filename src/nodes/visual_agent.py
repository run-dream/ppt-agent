import json
import os
import time
import dashscope
from dashscope import MultiModalConversation
from langchain_core.messages import HumanMessage
from src.models.state import PPTState
from src.utils.llm_factory import LLMFactory
from src.utils.prompt_manager import read_prompt
from src.utils.tools import search_real_photo, generate_creative_image
from src.utils.logger import logger

# 设置DashScope API URL
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def generate_image_with_dashscope(prompt: str) -> str:
    """
    使用DashScope multimodal-generation API生成图片
    """
    api_key = os.getenv("LLM_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        logger.error("DashScope API key not found")
        return ""

    messages = [
        {
            "role": "user",
            "content": [
                {"text": prompt}
            ]
        }
    ]

    # 重试逻辑：最多重试1次，遇到频率限制时等待5秒
    max_retries = 1
    retry_count = 0

    while retry_count <= max_retries:
        try:
            logger.info(f"Generating image with DashScope: {prompt[:50]}... (attempt {retry_count + 1})")
            response = MultiModalConversation.call(
                api_key=api_key,
                model="qwen-image-max",
                messages=messages,
                result_format='message',
                stream=False,
                watermark=False,
                prompt_extend=True,
                negative_prompt="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
                size='1664*928'
            )

            if response.status_code == 200:
                # 从响应中提取图片URL
                if hasattr(response, 'output') and response.output:
                    if hasattr(response.output, 'choices') and response.output.choices:
                        choice = response.output.choices[0]
                        if hasattr(choice, 'message') and choice.message:
                            content = choice.message.content
                            if content and isinstance(content, list) and len(content) > 0:
                                first_item = content[0]
                                if isinstance(first_item, dict) and 'image' in first_item:
                                    image_url = first_item['image']
                                    logger.info(f"Image generated successfully: {image_url}")
                                    return image_url
                logger.error("Unexpected response format from DashScope API")
                logger.error(f"Response structure: {response}")
                if hasattr(response, 'output'):
                    logger.error(f"Output attributes: {dir(response.output)}")
                return ""
            else:
                logger.error(f"DashScope API error: {response.status_code}")
                if hasattr(response, 'code'):
                    logger.error(f"Error code: {response.code}")
                if hasattr(response, 'message'):
                    logger.error(f"Error message: {response.message}")

                    # 检查是否是频率限制错误
                    error_message = str(response.message).lower()
                    if "rate limit" in error_message and retry_count < max_retries:
                        logger.warning(f"Rate limit exceeded, retrying in 5 seconds... (attempt {retry_count + 1})")
                        time.sleep(5)
                        retry_count += 1
                        continue
                    else:
                        return ""
                return ""
        except Exception as e:
            logger.exception(f"Exception during DashScope image generation (attempt {retry_count + 1})")

            # 检查是否是频率限制错误
            error_message = str(e).lower()
            if "rate limit" in error_message and retry_count < max_retries:
                logger.warning(f"Rate limit exceeded, retrying in 5 seconds... (attempt {retry_count + 1})")
                time.sleep(5)
                retry_count += 1
                continue
            else:
                return ""

    # 所有重试都失败
    logger.error("All retry attempts failed for DashScope image generation")
    return ""

def visual_agent_node(state: PPTState) -> PPTState:
    """
    视觉 Agent 节点：直接使用 AI 生成图片
    """
    slides = state.get("slides", [])
    if not slides:
        return state

    logger.info(f"Visual Agent: Generating AI images for {len(slides)} slides...")

    updated_slides = slides.copy()

    for i, slide in enumerate(updated_slides):
        logger.info(f"Visual Agent: Generating image for Slide {i+1}: {slide.title}")

        # 使用幻灯片的 image_query 作为 AI 生成图片的提示词
        prompt = slide.image_query or f"{slide.title} - {', '.join(slide.bullet_points)}"

        try:
            # 直接使用 DashScope API 生成图片
            image_url = generate_image_with_dashscope(prompt)

            if image_url and image_url.startswith("http"):
                slide.image_path = image_url
                logger.info(f"Visual Agent: Slide {i+1} got AI-generated image")
            else:
                logger.warning(f"Visual Agent: Failed to generate image for Slide {i+1}")
                # 使用占位图作为fallback (使用支持PNG的服务)
                slide.image_path = f"https://via.placeholder.com/600x400.png?text={prompt.replace(' ', '+')}"

        except Exception as e:
            logger.error(f"Visual Agent: Error generating image for slide {i+1}: {str(e)}")
            # 使用占位图作为fallback
            slide.image_path = f"https://placehold.co/600x400?text={prompt.replace(' ', '+')}"

    return {
        **state,
        "slides": updated_slides,
        "current_step": "final_render"
    }
