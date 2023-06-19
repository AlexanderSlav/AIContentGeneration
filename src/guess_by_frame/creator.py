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
        self.movie_search_engine = GoogleAPISceneEngine(
            config.guess_scene_params.num_scenes_to_search,
            config.env_variables.google_api_key,
            config.env_variables.google_cx,
        )
        self.config = config
        self.video_generator = VideoGenerator(config)
        self.scene_collector = SceneCollector()
        self.movie_name = None

    async def handle_message(self, message):
        movie_name = message.text
        self.movie_name = movie_name
        self.images = await self.movie_search_engine.search(self.movie_name)

        if not self.images:
            await self.bot.send_message(message.chat.id, "No images found.")
            return

        for image in self.images:
            markup = types.InlineKeyboardMarkup()
            confirm_btn = types.InlineKeyboardButton("✅", callback_data="confirm")
            next_btn = types.InlineKeyboardButton("❌", callback_data="next")
            markup.add(confirm_btn, next_btn)

            # send the image without downloading
            await self.bot.send_photo(message.chat.id, image.url, reply_markup=markup)

    async def handle_query(self, call):
        if call.data == "confirm":
            # download the image when it is confirmed
            image = self.images.pop(0)
            path = await self.movie_search_engine.download([image], download_path=self.config.guess_scene_params.download_path)

            scene = Scene(path_to_image=path, movie_name=self.movie_name) # call.message.photo[-1].file_id
            self.scene_collector.add_scene(scene)
            await self.bot.answer_callback_query(call.id, "Image confirmed.")

            # check if we have enough scenes and generate the video
            # if (
            #     len(self.scene_collector.get_scenes())
            #     >= self.movie_search_engine.num_frames_per_request
            # ):
                
            await self.generate_and_send_video(call.message.chat.id)

        elif call.data == "next":
            await self.bot.answer_callback_query(call.id, "Next image.")

    async def generate_and_send_video(self, chat_id: int):
        image_paths = [scene.path_to_image for scene in self.scene_collector.get_scenes()]
        print(image_paths)
        self.video_generator.generate_video(image_paths=image_paths)

        with open("output.mp4", "rb") as video:
            await self.bot.send_video(chat_id, video)
