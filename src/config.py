import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class EnvironmentVariables(BaseModel):
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_token = os.getenv("OPENAPI_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cx = os.getenv("GOOGLE_CX")


class Config(BaseModel):
    env_vairiables: EnvironmentVariables = EnvironmentVariables()
    app_name: str = "AIContentGenerator"
    download_path = "output_images/"
    num_frames_per_request = 10
    log_path = "logs/"
    log_level = "DEBUG"


config = Config()
