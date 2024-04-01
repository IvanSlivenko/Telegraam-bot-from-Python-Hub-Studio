import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from const import ALOOWED_UPDATES
from phrases import GRETING_PHRASES, FAREWELL_PHRASES

from handlers.user_private import user_private_router
from handlers.user_private_2 import user_private_router
from handlers.user_group import user_group_router


from common.bot_commands_list import private



#===========================================
# bot = Bot(token = TOKEN)
# bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)

#===========================================



#--------------------------------------------------------------------
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats()) # Видалення команд з меню
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALOOWED_UPDATES)

asyncio.run(main())
#--------------------------------------------------------------------