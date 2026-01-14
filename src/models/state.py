from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

class SlideContent(BaseModel):
    """单张幻灯片的内容结构"""
    title: str = Field(description="幻灯片标题")
    bullet_points: List[str] = Field(default_factory=list, description="幻灯片要点列表")
    image_query: Optional[str] = Field(None, description="建议的图片搜索关键词")
    image_path: Optional[str] = Field(None, description="最终下载或生成的图片本地路径")
    layout_type: str = Field(default="default", description="建议的版式类型")

class PPTOutline(BaseModel):
    """PPT 大纲结构"""
    title: str = Field(description="PPT 总标题")
    chapters: List[str] = Field(default_factory=list, description="章节或主要页面标题列表")

class PPTState(TypedDict):
    """LangGraph 全局状态定义"""
    # 原始输入
    input_text: str
    input_files: List[str]
    
    # 中间产物
    outline: Optional[PPTOutline]
    slides: List[SlideContent]
    
    # 状态控制
    current_step: str
    is_approved: bool
    error: Optional[str]
    generated_file: Optional[str]