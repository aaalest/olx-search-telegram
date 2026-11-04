import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from olx_search_telegram.config import config
from olx_search_telegram.handlers.menus import router as menu_router
from olx_search_telegram.services.client import SearchApiClient


async def main():
    logging.basicConfig(level=logging.INFO)

    redis = Redis.from_url(config.redis_url)
    storage = RedisStorage(redis=redis)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=storage)

    api_client = SearchApiClient(base_url=config.api_base_url)

    @dp.startup.register
    async def on_startup(dispatcher: Dispatcher) -> None:
        await api_client.start()
        dispatcher["api_client"] = api_client
        logging.info("SearchApiClient started.")

    @dp.shutdown.register
    async def on_shutdown(dispatcher: Dispatcher) -> None:
        await api_client.close()
        logging.info("SearchApiClient closed.")

    dp.include_router(menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
