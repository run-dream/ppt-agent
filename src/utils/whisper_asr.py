import os
from openai import OpenAI
from src.utils.logger import logger

class WhisperASR:
    """
    语音转录工具，支持 OpenAI Whisper 协议
    """
    
    @staticmethod
    def transcribe(audio_file_path: str) -> str:
        """
        将音频文件转录为文本
        """
        api_key = os.getenv("LLM_API_KEY")
        api_base = os.getenv("LLM_API_BASE")
        # 如果是阿里云，通常有专门的 ASR 接口，但如果走兼容模式：
        # dashscope 的兼容模式目前主要针对 Chat，Audio 可能需要单独处理。
        # 这里先提供一个基于标准 OpenAI 协议的实现
        
        try:
            client = OpenAI(api_key=api_key, base_url=api_base)
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=os.getenv("WHISPER_MODEL", "whisper-1"), 
                    file=audio_file
                )
            
            logger.info(f"Successfully transcribed audio: {audio_file_path}")
            return transcript.text
        except Exception as e:
            logger.error(f"Whisper transcription failed: {str(e)}")
            return ""
