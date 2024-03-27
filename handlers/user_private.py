from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from const import COMMANDS_LIST

user_private_router = Router()
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Доброго дня {message.from_user.full_name} - я віртуальний помічник ")

@user_private_router.message(Command('menu'))
async def menu_comands(message: types.Message):
        await message.answer('Тут буде меню')

@user_private_router.message(Command('cl'))
async def commands_list(message: types.Message):
        await message.answer(COMMANDS_LIST)
@user_private_router.message()# обробник подій без фільтрів розміщуємо після всіх інших обробників подій
async def echo(message: types.Message):
        await message.answer(message.text)