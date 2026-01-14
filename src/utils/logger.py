import logging
import sys
import os

def setup_logger(name: str = "ChatPPT"):
    """
    统一日志配置
    """
    logger = logging.getLogger(name)
    
    # 如果已经有 handler，说明已经初始化过，直接返回
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.INFO)
    
    # 控制台输出格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # 如果有需要，可以增加 File Handler
    # log_dir = "logs"
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    # fh = logging.FileHandler(os.path.join(log_dir, "app.log"))
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    
    return logger

# 全局默认 logger
logger = setup_logger()
