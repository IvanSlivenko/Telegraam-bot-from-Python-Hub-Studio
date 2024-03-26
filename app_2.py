import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from const import TOKEN
from phrases import GRETING_PHRASES, FAREWELL_PHRASES

#===========================================
bot = Bot(token = TOKEN)
dp = Dispatcher()
#===========================================

current_name = 'Шановний клієнт'

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Ви активували команду 'Start'")

@dp.message()# обробник подій без фільтрів розміщуємо після всіх інших обробників подій
async def echo(message: types.Message):

        await message.answer(f"{current_name},\n ваша фраза : '{message.text}' нам не зрозуміла. \n  Спробуйте короткі фрази на зразок: {GRETING_PHRASES} чи {FAREWELL_PHRASES}")
#--------------------------------------------------------------------
async def main():
    await dp.start_polling(bot)

asyncio.run(main())
#--------------------------------------------------------------------