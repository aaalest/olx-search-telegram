import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from olx_search_telegram.config import config
from olx_search_telegram.handlers.menus import router as menu_router


async def main():
    logging.basicConfig(level=logging.INFO)

    redis = Redis.from_url(config.redis_url)

    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=storage)

    dp.include_router(menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
