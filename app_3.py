import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_marker
# from middlewares.db import CounterMiddleware


from const import ALLOWED_UPDATES

from phrases import GRETING_PHRASES, FAREWELL_PHRASES

from handlers.user_private_2 import user_private_router
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router

from common.bot_commands_list import private

# load_dotenv(find_dotenv())





#===========================================
# bot = Bot(token = TOKEN)
bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
# bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []

# dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
dp = Dispatcher()





dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

#===========================================
async def on_startup(bot):
    run_params = False
    if run_params:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    print('Бот впав')


#--------------------------------------------------------------------
async def main():

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_marker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats()) # Видалення команд з меню
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
#--------------------------------------------------------------------