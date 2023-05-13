import os

from loguru import logger

from src.config import config

if not os.path.exists(config.log_path):
    os.makedirs(config.log_path)

log_file_path = os.path.join(config.log_path, "app.log")

logger.remove()
logger.add(
    log_file_path,
    rotation="1 MB",
    retention="3 days",
    level=config.log_level,
    format="{time} :: {level} :: {file}.{function} {message}",
)


def get_logger(name):
    return logger.bind(name=name)
