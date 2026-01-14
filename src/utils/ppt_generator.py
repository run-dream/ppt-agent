import os
import requests
from io import BytesIO
from pptx import Presentation
from src.models.state import PPTState, PPTOutline, SlideContent
from src.utils.layout_manager import LayoutManager
from src.utils.logger import logger

class PPTGenerator:
    """
    PPT 生成器：根据 PPTState 中的数据渲染并导出 .pptx 文件
    """
    
    def __init__(self, output_dir: str = "data/outputs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, state: PPTState) -> str:
        """
        根据状态生成 PPT 文件并返回文件路径
        """
        outline = state.get("outline")
        slides_data = state.get("slides", [])
        
        if not outline:
            raise ValueError("No outline found in state for PPT generation.")

        prs = Presentation()
        
        # 1. 创建标题页
        self._add_title_slide(prs, outline.title)
        
        # 2. 逐页创建幻灯片
        for slide_data in slides_data:
            self._add_content_slide(prs, slide_data)
            
        # 3. 保存文件
        safe_title = "".join([c for c in outline.title if c.isalnum() or c in (' ', '_')]).rstrip()
        filename = f"{safe_title or 'presentation'}.pptx"
        file_path = os.path.join(self.output_dir, filename)
        
        prs.save(file_path)
        logger.info(f"PPT successfully generated at: {file_path}")
        return file_path

    def _add_title_slide(self, prs, title_text: str):
        layout = prs.slide_layouts[LayoutManager.get_layout_index("title_slide")]
        slide = prs.slides.add_slide(layout)
        title_ph = LayoutManager.get_placeholder(slide, 'title')
        if title_ph:
            title_ph.text = title_text

    def _add_content_slide(self, prs, data: SlideContent):
        layout_idx = LayoutManager.get_layout_index(data.layout_type)
        layout = prs.slide_layouts[layout_idx]
        slide = prs.slides.add_slide(layout)
        
        # 填充标题
        title_ph = LayoutManager.get_placeholder(slide, 'title')
        if title_ph:
            title_ph.text = data.title
            
        # 填充正文
        body_ph = LayoutManager.get_placeholder(slide, 'body')
        if body_ph:
            tf = body_ph.text_frame
            tf.clear() # 清除默认占位符文本
            for point in data.bullet_points:
                p = tf.add_paragraph()
                p.text = point
                p.level = 0
                
        # 填充图片 (如果有路径或 URL)
        if data.image_path:
            self._add_image(slide, data.image_path)

    def _add_image(self, slide, image_source: str):
        """添加图片到幻灯片，支持本地路径或 URL"""
        pic_ph = LayoutManager.get_placeholder(slide, 'picture')
        
        try:
            if image_source.startswith(('http://', 'https://')):
                # 处理远程图片
                response = requests.get(image_source, timeout=10)
                image_data = BytesIO(response.content)
            elif os.path.exists(image_source):
                # 处理本地图片
                image_data = image_source
            else:
                logger.warning(f"Image source not found: {image_source}")
                return

            if pic_ph:
                pic_ph.insert_picture(image_data)
            else:
                # 如果没有图片占位符，默认在右下角放一个小图 (非理想，但可以作为 fallback)
                # 或者可以使用 slide.shapes.add_picture(image_data, left, top, width, height)
                logger.debug("No picture placeholder found in layout, skipping auto-insert.")
        except Exception as e:
            logger.error(f"Failed to add image to slide: {str(e)}")

def ppt_generator_node(state: PPTState) -> PPTState:
    """
    PPT 渲染节点：最终生成 .pptx 文件并记录路径
    """
    logger.info("PPT Generator Node: Starting rendering...")
    generator = PPTGenerator()
    
    try:
        file_path = generator.generate(state)
        # 将生成的文件路径存入 state (需要更新状态定义以支持 file_path)
        # 或者我们暂时存入 error 作为传递手段，或者直接返回
        return {
            **state,
            "generated_file": file_path,
            "current_step": "completed"
        }
    except Exception as e:
        logger.exception("PPT Generator Node: Failed to render PPT.")
        return {
            **state,
            "error": f"Error in PPT generator: {str(e)}"
        }
