import logging
import os
import sys
import datetime


# 颜色代码
class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# 创建日志目录
def ensure_log_dir():
    """确保日志目录存在"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


# 自定义日志格式处理器
class ColoredFormatter(logging.Formatter):
    """自定义格式处理器，为不同级别的日志添加颜色"""

    FORMATS = {
        logging.DEBUG: Colors.CYAN
        + "%(asctime)s - %(levelname)s - %(message)s"
        + Colors.RESET,
        logging.INFO: Colors.GREEN
        + "%(asctime)s - %(levelname)s - %(message)s"
        + Colors.RESET,
        logging.WARNING: Colors.YELLOW
        + "%(asctime)s - %(levelname)s - %(message)s"
        + Colors.RESET,
        logging.ERROR: Colors.RED
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Colors.RESET,
        logging.CRITICAL: Colors.RED
        + Colors.BOLD
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Colors.RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# 获取日志对象
def get_logger(name, log_to_file=False, level=logging.INFO):
    """获取配置好的日志对象

    Args:
        name: 日志名称，通常是模块名
        log_to_file: 是否同时记录到文件
        level: 日志级别，默认INFO

    Returns:
        logging.Logger: 配置好的日志对象
    """
    logger = logging.getLogger(name)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # 控制台处理器
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(ColoredFormatter())
    logger.addHandler(console_handler)

    # 文件处理器
    if log_to_file:
        log_dir = ensure_log_dir()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"{today}.log")

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # 阻止日志传递到根日志器
    logger.propagate = False

    return logger


# 主应用日志器
app_logger = get_logger("jellyfin-library-poster", log_to_file=True)


# 获取模块特定的日志器
def get_module_logger(module_name):
    """获取模块特定的日志器

    Args:
        module_name: 模块名称

    Returns:
        logging.Logger: 配置好的日志对象
    """
    return get_logger(f"jellyfin-library-poster.{module_name}")
