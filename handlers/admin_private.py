from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_change_banner_image,
    orm_get_categories,
    orm_add_product,
    orm_delete_product,
    orm_get_info_pages,
    orm_get_product,
    orm_get_products,
    orm_update_product,
)

from filters.chat_types import ChatTypeFilter, IsAdmin

from kbds.inline import get_callback_btns
from kbds.reply_2 import get_keyboard




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

@admin_router.message(F.text == 'Асортимент')
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name: f'category_{category.id}' for category in categories}
    await message.answer("Оберіть категорію", reply_markup=get_callback_btns(btns=btns))


@admin_router.callback_query(F.data.startswith('category_'))
async def starring_at_product(callback: types.callback_query, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n {product.description}\n Вартість : {round(product.price, 2)}",
            reply_markup=get_callback_btns(btns={
                'Видалити': f'delete_{product.id}',
                'Змінити': f'change_{product.id}'
            })
        )
    await callback.answer()
    await callback.message.answer('ОК, ось список товарів')

# ----- Видаляємо товар
@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product_callback(
        callback: types.CallbackQuery, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар видалено", show_alert=True)
    await callback.message.answer("Товар видалено !")

############ Мікро FSM для  завантаження / зміни банерів#################
class AddBanner(StatesGroup):
    image = State()


# Відправляємо перелік інформаційних сторінок бота і стаємо в стан відправки фото
@admin_router.message(StateFilter(None), F.text == 'Додати/Змінити банер')
async def add_image_2(message: types.message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f"Відправте фото банера.\nВ описі вкажіть для якої сторінки:\
                         \n{','.join(pages_names)}")
    await state.set_state(AddBanner.image)

#Додаємо / Змінюємо зображення в таблиці (там уже є записані сторінки по іменам:
# main, catalog, cart(для пустої корзини),about, payment, shipping)

@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_name = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_name:
        await message.answer(f"Введіть нормальну назву сторінки:\
                            \n{','.join(pages_name)}")
        return
    await orm_change_banner_image(session, for_page, image_id)
    await message.answer("Банер додано / змінено.")
    await state.clear()

#Ловимо не коректне введення
@admin_router.message(AddBanner.image)
async def add_banner_2(message: types.Message, state: FSMContext):
    await message.answer("Відправте фото банера чи натисніть відміну")
########################################################################################

class AddProduct(StatesGroup):
    #Кроки станів
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()

    product_change = None

    texts = {
        "AddProduct:name": "Введіть назву заново",
        "AddProduct:description": "Введіть опис заново",
        "AddProduct:category": "Введіть категорію заново",
        "AddProduct:price": "Введіть ціну заново",
        "AddProduct:image": "Цей крок останній",

    }




# Код для машин стану (FSM) ////////////////////////////////////////////////////

# ------- Змінюємо товар
# Заходимо в стан очікування вводу ім'я (при зміні)
@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    # await callback.answer()
    await callback.message.answer(
        "Введіть назву товару", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


# -------------Додаємо товар
# Заходимо в стан очікування вводу ім'я (при додаванні)
@admin_router.message(StateFilter(None), F.text == "Додати товар")
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
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
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


#Ловимо данні для стану name та змінюємо стан на description
@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_for_change:
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        if 4 >= len(message.text) >=150:
            await message.answer("Назва товара має містити від 4 до 150 символів")
            return
        await state.update_data(name=message.text)
    await message.answer("Додайте опис товару")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def add_name_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали недопустимі данні, вкажіть назву товару у строковому форматі")

#Ловимо данні для стану description та змінюємо стан на price
@admin_router.message(AddProduct.description,F.text)
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == '.' and AddProduct.product_for_change:
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        if 4 >= len(message.text):
            await message.answer(
                "Занадто короткий опис.\n Напишіть знову"
            )
            return
        await state.update_data(description=message.text)
    categories = await orm_get_categories(session)
    btns = {category.name: str(category.id) for category in categories}
    await message.answer("Оберіть категорію", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddProduct.category)
@admin_router.message(AddProduct.description)
async def add_description_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть опис товару у строковому форматі")


@admin_router.message(AddProduct.price, or_f(F.text, F.text == '.'))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введіть коректне значення ціни")
            return


        await state.update_data(price=message.text)
    await message.answer("Додайте картинку товару")
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price)
async def add_price_Error(message: types.Message, state: FSMContext):
    await message.answer("Ви вказали не допустимі данні, вкажіть ціну товару у числовому форматі")


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == '.'))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    if message.text and message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Товар додано/змінено", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
        f"Помилка: \n{str(e)}\n Зверніться до розробника", reply_markup=ADMIN_KB)
        await state.clear()

    AddProduct.product_for_change = None

@admin_router.message(AddProduct.image)
async def add_price_Error(message: types.Message, state: FSMContext):
    await message.answer("Додайте зображення товару")


#//////////////////////////////////////////////////////////////////////////////
# @admin_router.message(AddProduct.name, or_f(F.text, F.text == '.') )
# async def add_name(message: types.Message, state: FSMContext):
#     if message.text == '.':
#         await state.update_data(name=AddProduct.product_for_change.name)
#     else:
#         if len(message.text) >= 100:
#             await message.answer(
#                 'Назва товару не повина перевищувати 100 символів.\n Спробуйте знову'
#             )
#             return
#
#         await state.update_data(name=message.text)
#     await message.answer("Вкажіть опис товару")
#     await state.set_state(AddProduct.description)
#/////////////////////////////////////////////////////////////////////////////////////////

# @admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
# async def add_description(message: types.Message, state: FSMContext):
#     if message.text == '.':
#         await state.update_data(description=AddProduct.product_for_change.description)
#     else:
#         await state.update_data(description=message.text)
#     await message.answer("Вкажіть ціну товару")
#     await state.set_state(AddProduct.price)
