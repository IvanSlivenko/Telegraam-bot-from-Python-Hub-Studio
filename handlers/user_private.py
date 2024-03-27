from aiogram import types, Router
from aiogram.filters import CommandStart

user_private_router = Router()
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"{message.from_user.full_name} - Ви активували команду 'Start'")

@user_private_router.message()# обробник подій без фільтрів розміщуємо після всіх інших обробників подій
async def echo(message: types.Message):
        await message.answer(message.text)