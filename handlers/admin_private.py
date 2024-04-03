from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply_2 import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
        "Додати товар",
        "Змінити товар",
        "Видалити товар",
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

# Код для машин стану (FSM) ////////////////////////////////////////////////////

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    texts = {
        'AddProduct:name': 'Вкажіть назву заново',
        'AddProduct:description': 'Вкажіть опис заново',
        'AddProduct:price': 'Вкажіть ціну заново',
        'AddProduct:image': 'Цей крос останній...'

    }

@admin_router.message(StateFilter(None),F.text.lower() == "додати товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Вкажіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command("відміна"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Дії відмінені", reply_markup=ADMIN_KB)

@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer("Попередього кроку немає, або вкажіть назву товара, або напишіть 'відміна'")
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, ви повернулись до попереднього кроку \n {AddProduct.texts[previous.state]}")
            return
        previous = step

    await message.answer(f"ок, ви повернулись до попереднього кроку")

@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Вкажіть опис товару")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть назву товару у строковому форматі")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Вкажіть ціну товару")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)
async def add_description_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть опис товару у строковому форматі")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Додайте картинку товару")
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price)
async def add_price_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть ціну товару у числовому форматі")


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Товар додано", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@admin_router.message(AddProduct.image)
async def add_price_Error(message: types.Message, state: FSMContext):
    await message.answer("Додайте зображення товару")

