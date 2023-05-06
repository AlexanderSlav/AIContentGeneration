import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    app_name: str = "AIContentGenerator"
    log_path = os.getenv("LOG_PATH", "logs/")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_token = os.getenv("OPENAPI_KEY")


config = Config()
