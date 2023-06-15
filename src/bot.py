from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from src.config import Config
from src.constants import ContentTypeRequest, StateKeys
from src.guess_by_frame.creator import GuessSceneRoundCreator
from src.guess_by_music.creator import GuessMusicRoundCreator
from src.logger import get_logger

logger = get_logger(__name__)


class QuizBot:
    def __init__(self):
        self.config = Config()
        self.bot = Bot(token=self.config.env_variables.telegram_bot_token)
        self.dp = Dispatcher(self.bot)

        self.handler = GuessSceneRoundCreator(self.bot, self.config)

    async def handle_message(self, message: types.Message):
        logger.info("Handling message")
        await self.handler.handle_message(message)

    async def handle_query(self, call: types.CallbackQuery):
        logger.info("Handling query")
        await self.handler.handle_query(call)

    async def send_intro(self, message: types.Message):
        movie_scene_btn = types.InlineKeyboardButton(
            "🎬 Get scene from movie",
            callback_data=ContentTypeRequest.guess_by_scene.value,
        )
        markup = types.InlineKeyboardMarkup().add(movie_scene_btn)
        await self.bot.send_message(
            message.chat.id, "Choose an option:", reply_markup=markup
        )

    async def run(self):
        self.dp.register_message_handler(
            self.send_intro, commands=["start", "hello", "intro"]
        )
        self.dp.register_message_handler(
            self.handle_message, content_types=types.ContentTypes.TEXT
        )
        self.dp.register_callback_query_handler(self.handle_query)
        logger.info("Bot is running")
        await self.dp.start_polling()
