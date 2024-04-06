from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply_2 import get_keyboard
from kbds.inline import get_inlineMix_btns, get_callback_btns, get_url_btns
from database.orm_query import orm_product, orm_get_products, orm_get_product , orm_delete_product, orm_update_product




admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = get_keyboard(
        "Додати товар",
        "Ассортимент",
        placeholder="Оберіть дію",
        sizes=(2,),
    )
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Вкажіть назву заново',
        'AddProduct:description': 'Вкажіть опис заново',
        'AddProduct:price': 'Вкажіть ціну заново',
        'AddProduct:image': 'Цей крос останній...'

    }
@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Маєте бажання щось зробити", reply_markup=ADMIN_KB)

@admin_router.message(F.text == 'Ассортимент')
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n {product.description}\n Вартість : {round(product.price, 2)}",
            reply_markup=get_callback_btns(btns={
                'Видалити': f'delete_{product.id}',
                'Змінити': f'change_{product.id}'
            })
        )
    await message.answer('ОК, ось список товарів')

# ----- Видаляємо товар
@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар видалено", show_alert=True)
    await callback.message.answer("Товар видалено !")


# ------- Змінюємо товар
@admin_router.callback_query(StateFilter(None), F.data.startwith("change_"))
async def change_product_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change
    await callback.answer("Товар буде змінено", show_alert=True)
    await callback.message.answer(
        "Введіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


# Код для машин стану (FSM) ////////////////////////////////////////////////////


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

@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.') )
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change)
    else:
        if len(message.text) >= 100:
            await message.answer('Назва товру не повина перевищувати 100 символів.\n Спробуйте знову')
            return

        await state.update_data(name=message.text)
    await message.answer("Вкажіть опис товару")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть назву товару у строковому форматі")


@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
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
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        await orm_product(session, data)
        await message.answer("Товар додано", reply_markup=ADMIN_KB)
        await state.clear()
    except Exception as e:
        await message.answer(
        f"Помилка: \n{str(e)}\n Зверніться до розробника", reply_markup=ADMIN_KB)
        await state.clear()



@admin_router.message(AddProduct.image)
async def add_price_Error(message: types.Message, state: FSMContext):
    await message.answer("Додайте зображення товару")

