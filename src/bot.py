import telebot
from telebot import types

from src.config import config
from src.guess_by_frame.google_api import GoogleAPISceneEngine

confirmed_images = []


class MovieBot:
    def __init__(self, bot, api_key, cx, download_path):
        self.bot = bot
        self.api_key = api_key
        self.cx = cx
        self.download_path = download_path
        self.movie_engine = None
        self.images = None
        self.confirmed_images = []
        self.image_counter = 0

    def handle_movie(self, message):
        movie_name = " ".join(message.text.split()[1:])
        self.movie_engine = GoogleAPISceneEngine(movie_name, 5, self.api_key, self.cx)
        self.image_counter = 0
        self.send_image(message.chat.id)

    def send_image(self, chat_id):
        if self.images is None or len(self.images) == 0:
            self.images = self.movie_engine.download(self.download_path)
        if (
            self.images is None
            or len(self.images) == 0
            or self.image_counter >= self.movie_engine.num_frames_per_request
        ):
            self.bot.send_message(chat_id, "No more images.")
            return
        image = self.images.pop(0)
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton("✅", callback_data="confirm")
        next_btn = types.InlineKeyboardButton("❌", callback_data="next")
        markup.add(confirm_btn, next_btn)
        with open(f"{self.download_path}/{image.path}", "rb") as img:
            self.bot.send_photo(chat_id, img, reply_markup=markup)
            self.image_counter += 1

    def handle_query(self, call):
        if call.data == "confirm":
            self.confirmed_images.append(call.message.photo[-1].file_id)
            self.bot.answer_callback_query(call.id, "Image confirmed.")
        elif call.data == "next":
            self.bot.answer_callback_query(call.id, "Next image.")
        if self.image_counter < self.movie_engine.num_frames_per_request:
            self.send_image(call.message.chat.id)


bot = telebot.TeleBot(config.env_vairiables.telegram_bot_token)

movie_bot = MovieBot(
    bot,
    config.env_vairiables.google_api_key,
    config.env_vairiables.google_cx,
    config.download_path,
)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hi, I'm a bot that can generate a scene from a movie."
        "Send me a movie name. For example: /get_scene_from_movie The Matrix",
    )


@bot.message_handler(commands=["get_scene_from_movie"])
def handle_movie(message):
    movie_bot.handle_movie(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    movie_bot.handle_query(call)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
