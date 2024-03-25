import asyncio
from aiogram import Bot, Dispatcher, types

from const import TOKEN

bot = Bot(token = TOKEN)

dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

asyncio.run(main())