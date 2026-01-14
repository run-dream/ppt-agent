import os

def read_prompt(prompt_name: str) -> str:
    """
    从 src/prompts/ 目录下读取指定的 prompt 文本文件
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    prompt_path = os.path.join(project_root, "prompts", f"{prompt_name}.txt")
    
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()
