from aiogram import F, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply_2 import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
        "Додати товар",
        "Змінити товар",
        "видалити товар",
        "Я так, просто подивитись",
        placeholder="Оберіть дію",
        sizes=(2, 1, 1),
    )

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Маєте бажання щось зробити", reply_markup=ADMIN_KB)

@admin_router.message(F.text.lower() == 'я так просто подивитись')
async def starring_at_product(message: types.Message):
    await message.answer('ОК , ось список товарів')



@admin_router.message(F.text.lower() == 'змінити товар')
async def change_product(message: types.Message):
    await message.answer('ОК , ось список товарів')


@admin_router.message(F.text.lower() == "видалити товар")
async def delete_product(message: types.Message):
    await message.answer("Виберіть товар(и) для видалення")


@admin_router.message(F.text.lower() == "додати товар")
async def add_product(message: types.Message):
    await message.answer(
        "Вкажіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )

@admin_router.message(Command("відміна"))
@admin_router.message(F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message) -> None:
    await message.answer("Дії відмінені", reply_markup=ADMIN_KB)

@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def cancel_handler(message: types.Message) -> None:
    await message.answer(f"ок, ви повернулись до попереднього кроку")

@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer("Вкажіть iм'я товару")

@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer("Вкажіть опис товару")

@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer("Вкажіть ціну товару")

@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer("Завантажте зображення товару")
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)

