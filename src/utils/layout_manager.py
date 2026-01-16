from pptx.enum.shapes import PP_PLACEHOLDER
from src.utils.logger import logger

class LayoutManager:
    """
    PPT 版式管理器：负责将系统建议的版式类型映射为 python-pptx 的内置版式。
    
    默认版式索引参考 (Standard PPT Layouts):
    0: Title (标题页)
    1: Title and Content (标题 + 内容)
    2: Section Header (章节页)
    3: Two Content (两栏内容)
    4: Comparison (比较)
    5: Title Only (仅标题)
    6: Blank (空白)
    7: Content with Caption (内容 + 说明)
    8: Picture with Caption (图片 + 说明)
    """
    
    # 映射表：抽象版式名称 -> pptx 索引
    LAYOUT_MAPPING = {
        "title_slide": 0,      # Title - 只有标题
        "title_content": 8,    # Picture with Caption - 有标题、内容和图片占位符
        "section_header": 2,   # Section Header
        "two_column": 3,       # Two Content
        "comparison": 4,       # Comparison
        "title_only": 5,       # Title Only
        "blank": 6,            # Blank
        "content_caption": 7,  # Content with Caption
        "picture_caption": 8,  # Picture with Caption - 有图片占位符
        "default": 8           # 默认使用有图片的布局
    }

    @staticmethod
    def get_layout_index(layout_name: str) -> int:
        """根据名称获取版式索引"""
        layout_idx = LayoutManager.LAYOUT_MAPPING.get(layout_name, 8)  # 默认使用有图片的布局
        # 确保索引在有效范围内 (0-8)
        return max(0, min(layout_idx, 8))

    @staticmethod
    def get_placeholder(slide, placeholder_type):
        """
        根据类型获取幻灯片中的占位符
        placeholder_type: 'title', 'body', 'picture'
        """
        for shape in slide.placeholders:
            if placeholder_type == 'title' and shape.placeholder_format.type == PP_PLACEHOLDER.TITLE:
                return shape
            if placeholder_type == 'body' and (shape.placeholder_format.type == PP_PLACEHOLDER.BODY or shape.placeholder_format.type == PP_PLACEHOLDER.OBJECT):
                return shape
            if placeholder_type == 'picture' and shape.placeholder_format.type == PP_PLACEHOLDER.PICTURE:
                return shape
        return None
