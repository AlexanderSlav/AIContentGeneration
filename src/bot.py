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


class QuizForm(StatesGroup):
    waiting_for_game_type = State()
    waiting_for_movie_name = State()


class QuizBot:
    def __init__(self):
        self.config = Config()
        self.bot = Bot(token=self.config.env_variables.telegram_bot_token)
        storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=storage)

        self.handlers = {
            ContentTypeRequest.guess_by_scene.value: GuessSceneRoundCreator(
                self.bot, self.config
            ),
            ContentTypeRequest.guess_by_music_theme.value: GuessMusicRoundCreator(
                self.bot, self.config
            ),
        }

    async def handle_message(self, message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        data = await state.get_data()
        game_type = data.get(StateKeys.GAME_TYPE.value)

        if current_state == QuizForm.waiting_for_movie_name.state and game_type:
            handler = self.handlers[game_type]
            await handler.handle_message(message)
            await state.finish()  # reset the state when done
        else:
            await message.reply(
                "I didn't understand that. Please choose an option from the menu."
            )

    async def handle_query(self, call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        if game_type := data.get(StateKeys.GAME_TYPE.value):
            handler = self.handlers[game_type]
            await handler.handle_query(call)
            await state.finish()  # reset the state when done
        elif call.data in self.handlers:
            await self.bot.send_message(
                call.message.chat.id, "Send me a movie name. For example: The Matrix"
            )
            await QuizForm.waiting_for_game_type.set()
            await state.update_data({StateKeys.GAME_TYPE.value: call.data})
            await QuizForm.waiting_for_movie_name.set()  # add this line
        else:
            await self.bot.answer_callback_query(
                call.id, "This feature is not implemented yet."
            )

    async def send_intro(self, message: types.Message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        movie_scene_btn = types.InlineKeyboardButton(
            "🎬 Get scene from movie",
            callback_data=ContentTypeRequest.guess_by_scene.value,
        )
        movie_dialogue_btn = types.InlineKeyboardButton(
            "💬 Get dialogue for movie",
            callback_data=ContentTypeRequest.guess_by_dialogue.value,
        )
        movie_music_btn = types.InlineKeyboardButton(
            "🎵 Get music theme for movie",
            callback_data=ContentTypeRequest.guess_by_music_theme.value,
        )
        markup.add(movie_scene_btn, movie_dialogue_btn, movie_music_btn)
        logger.info("Intro processed")
        await self.bot.send_message(
            message.chat.id, "Choose an option:", reply_markup=markup
        )

    async def run(self):
        self.dp.register_message_handler(
            self.send_intro, commands=["start", "hello", "intro"]
        )
        self.dp.register_message_handler(
            self.handle_message,
            state=[QuizForm.waiting_for_movie_name, QuizForm.waiting_for_game_type],
            content_types=types.ContentTypes.TEXT,
        )
        self.dp.register_callback_query_handler(self.handle_query, state="*")

        logger.info("Bot is running")
        await self.dp.start_polling()
