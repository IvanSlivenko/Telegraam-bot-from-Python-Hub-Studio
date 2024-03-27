import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from const import TOKEN
from phrases import GRETING_PHRASES, FAREWELL_PHRASES
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())



#===========================================
# bot = Bot(token = TOKEN)
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
#===========================================

# current_name = 'Шановний клієнт'

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"{message.from_user.full_name} - Ви активували команду 'Start'")

@dp.message()# обробник подій без фільтрів розміщуємо після всіх інших обробників подій
async def echo(message: types.Message, bot:Bot):
        # await bot.send_message(message.from_user.id, 'Відповідь')
        # await message.answer(f"{message.from_user.full_name} - ,\n ваша фраза : '{message.text}' нам не зрозуміла. \n  Спробуйте короткі фрази на зразок: {GRETING_PHRASES} чи {FAREWELL_PHRASES}")
        await message.answer(message.text)
        await message.reply(message.text)
#--------------------------------------------------------------------
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
#--------------------------------------------------------------------