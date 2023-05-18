import os
import sys

from loguru import logger

from src.config import Config

config = Config()

if not os.path.exists(config.logging_params.log_path):
    os.makedirs(config.logging_params.log_path)

logger.remove()


logger.add(
    config.logging_params.log_file_path,
    rotation="00:00",  # Create a new log file every day at midnight
    retention="7 days",  # Keep log files for 7 days
    level=config.logging_params.log_level,
    format="{time} :: {level} :: {file}.{function} {message}",
    serialize=False,
)

# Add logging to console (standard output)
logger.add(
    sys.stdout,
    level=config.logging_params.log_level,
    format="{time} :: {level} :: {file}.{function} {message}",
)


def get_logger(name):
    return logger.bind(name=name)
