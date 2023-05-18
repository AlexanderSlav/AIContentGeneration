import os
from datetime import datetime

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class LoggingConfig(BaseModel):
    log_path: str = "logs/"
    log_level: str = "DEBUG"

    @property
    def log_file_path(self):
        timestamp = datetime.now().strftime("%d_%m_%Y")
        return os.path.join(self.log_path, f"log_{timestamp}.txt")


class EnvironmentVariables(BaseModel):
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_token = os.getenv("OPENAPI_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cx = os.getenv("GOOGLE_CX")


class OutputVideoParameters(BaseModel):
    fps: int = 1
    images_path: str = "output_images/"
    output_path: str = "output_video.mp4"
    music_path: str = "data/thinking_time.mp3"
    output_video_codec: str = "libx264"


class GuessSceneParameters(BaseModel):
    num_scenes_per_round: int = 10
    num_scenes_to_search: int = 5
    download_path: str = "output_images"


class Config(BaseModel):
    app_name: str = "AIContentGenerator"
    env_variables: EnvironmentVariables = EnvironmentVariables()
    logging_params: LoggingConfig = LoggingConfig()
    guess_scene_params: GuessSceneParameters = GuessSceneParameters()
    out_video_params: OutputVideoParameters = OutputVideoParameters(
        images_path=guess_scene_params.download_path
    )
