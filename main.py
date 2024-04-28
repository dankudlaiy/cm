import asyncio
import common

from aiogram import Dispatcher

from routers.default_router import default_router

dp = Dispatcher()

bot = common.bot


async def main():
    print('bot polling')
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(default_router)
    asyncio.run(main())
