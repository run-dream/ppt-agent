import docx
from src.utils.logger import logger

class DocxParser:
    """
    Word 文档解析工具，用于从 .docx 文件中提取内容
    """
    
    @staticmethod
    def parse(file_path: str) -> str:
        """
        解析 docx 文件并返回合并后的文本
        """
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            
            content = "\n".join(full_text)
            logger.info(f"Successfully parsed docx: {file_path}, length: {len(content)}")
            return content
        except Exception as e:
            logger.error(f"Failed to parse docx {file_path}: {str(e)}")
            return ""
