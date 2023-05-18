import asyncio

from src.bot import QuizBot
from src.logger import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":
    quiz_bot = QuizBot()
    logger.info("=" * 100)
    asyncio.run(quiz_bot.run())
