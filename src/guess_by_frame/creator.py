from typing import List

from aiogram import types

from src.config import Config
from src.guess_by_frame.utils import Scene, SceneCollector
from src.image_search_engine.google_api import GoogleAPISceneEngine
from src.logger import get_logger
from src.video_utils import VideoGenerator

logger = get_logger(__name__)


class GuessSceneRoundCreator:
    def __init__(self, bot, config: Config):
        self.bot = bot
        self.api_key: str = config.env_variables.google_api_key
        self.cx: str = config.env_variables.google_cx
        self.output_video_path: str = config.out_video_params.output_path
        self.download_path: str = config.guess_scene_params.download_path
        self.num_scenes_per_round: str = config.guess_scene_params.num_scenes_per_round
        self.num_scenes_to_search: str = config.guess_scene_params.num_scenes_to_search
        self.movie_search_engine: GoogleAPISceneEngine = GoogleAPISceneEngine(
            self.num_scenes_to_search, self.api_key, self.cx
        )
        self.video_generator = VideoGenerator(config)
        self.scene_collector: SceneCollector = SceneCollector()
        self.image_counter: int = 0

    async def handle_message(self, message):
        self.movie_name = message.text
        self.image_counter = 0
        self.images = await self.movie_search_engine.search(self.movie_name)

        if not self.images or len(self.images) == 0:
            await self.bot.send_message(message.chat.id, "No more images.")
            return

        for image in self.images:
            if self.image_counter >= self.movie_search_engine.num_frames_per_request:
                break

            logger.debug(f"Sending image {self.image_counter}")
            markup = types.InlineKeyboardMarkup()
            confirm_btn = types.InlineKeyboardButton("✅", callback_data="confirm")
            next_btn = types.InlineKeyboardButton("❌", callback_data="next")
            markup.add(confirm_btn, next_btn)

            # send the image without downloading
            await self.bot.send_photo(message.chat.id, image.url, reply_markup=markup)
            self.image_counter += 1

    async def handle_query(self, call):
        logger.info(f"Callback query: {call}")
        if call.data == "confirm":
            # download the image when it is confirmed
            image = self.images.pop(0)
            await self.movie_search_engine.download([image], self.download_path)

            logger.info("DEBUG", call.message.photo[-1].file_id, call.message.caption)
            print(call.message.photo[-1].file_id, call.message.caption)
            scene = Scene(call.message.photo[-1].file_id, call.message.caption)
            self.scene_collector.add_scene(scene)
            await self.bot.answer_callback_query(call.id, "Image confirmed.")
        elif call.data == "next":
            await self.bot.answer_callback_query(call.id, "Next image.")
        if (
            self.movie_search_engine
            and self.image_counter < self.movie_search_engine.num_frames_per_request
        ):
            await self.handle_message(call.message)

    def parse_scenes(self, scenes: List[Scene]) -> List[str]:
        return [scene.image_path for scene in scenes]

    async def generate_and_send_video(self, chat_id: int, music_path: str):
        image_paths = self.parse_scenes(self.scene_collector.get_scenes())
        self.video_generator.generate_video(image_paths=image_paths)

        with open("output.mp4", "rb") as video:
            await self.bot.send_video(chat_id, video)
