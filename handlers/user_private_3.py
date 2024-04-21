from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import (
    orm_add_product,
    orm_get_products,
    orm_add_to_cart,
    orm_add_user,

)


from filters.chat_types import ChatTypeFilter
from kbds.inline import get_callback_btns, MenuCallBack
from handlers.menu_processing import get_menu_content

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )


    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Toвар додано до кошика")
@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):

    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,


    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()



    # #--------------------------------------------------
    # await message.answer(
    #     f"Доброго дня {message.from_user.full_name} - я віртуальний помічник ",
    #          reply_markup=get_callback_btns(btns={
    #                 'Тисни сюди': 'some_1'
    #         }))
    #-------------------------------------------------

#-------------------------------------------------------------------------------------
# @user_private_router.callback_query(F.data.startswith('some_'))
# async def counter(callback: types.CallbackQuery):
#     number = int(callback.data.split('_')[-1])
#
#
#     await callback.message.edit_text(
#         text=f"Натиснутий - {number}",
#         reply_markup=get_callback_btns(btns={
#             'Тисни ще раз': f'some_{number + 1}'
#         }))

#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------
# @user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
# async def menu_comands(message: types.Message, session: AsyncSession):
#     for product in await orm_get_products(session):
#         await message.answer_photo(
#             product.image,
#             caption=f"<strong>{product.name}\
#                     </strong>\n {product.description}\n Вартість : {round(product.price, 2)}",
#         )
#     await message.answer('Ось меню')
# @user_private_router.message(Command('cl'))
# async def commands_list(message: types.Message):
#         await message.answer(COMMANDS_LIST)
#
#
# @user_private_router.message((F.text.lower().contains('про нас')) | (F.text.lower().contains('знайти')))
# @user_private_router.message(Command('about'))
# async def about_cmd(message: types.Message):
#         await message.answer('Про нас')
#
# @user_private_router.message((F.text.lower().contains('оплат')) | (F.text.lower() == 'варіанти оплати') | (F.text.lower().contains('заплат')))
# @user_private_router.message(Command('payment'))
# async def payment_cmd(message: types.Message):
#     text = as_marked_section(
#         Bold("Варіанти оплати:"),
#         'Карткою в боті',
#         'При отриманні',
#         'В закладі',
#         marker='✔ '
#
#     )
#     # await message.answer('З приводу оплати вам розповість менеджер з продажу 067 470 87 21')
#     await message.answer(text.as_html())
#
#
# @user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варіанти доставки'))
# @user_private_router.message(Command('shipping'))
# async def magic_filter_text_contains(message: types.Message):
#     text = as_list(as_marked_section(
#             Bold("Варіанти доставки:"),
#             "Кур'єр (доставка)",
#             'Самовиніс (з собою )',
#             'В закладі (тут )',
#             marker='✔ '
#             ),
#             as_marked_section(
#                 Bold("Не можна:"),
#                 "Пошта",
#                 'Голуби',
#
#                 marker='❌ '
#             ),
#             sep='\n-----------------------------------\n'
#     )
#     # await message.answer('<b>З питань доставки уточніть у логіста 067 470 87 21</b>', parse_mode=ParseMode.HTML)
#     await message.answer(text.as_html())
#
# @user_private_router.message((F.text.lower() == 'привіт') |
#                              (F.text.lower() == 'доброго дня') |
#                              (F.text.lower() == 'добрий день'))
# async def magic_filter_text_greeting(message: types.Message):
#         await message.answer(f'Вітаємо Вас \n{message.from_user.first_name}')
#
# @user_private_router.message( (F.text.lower().contains('замовити')) | (F.text.lower().contains('замовлення')) )
# async def magic_filter_text_order(message: types.Message):
#         await message.answer('З приводу замовлень уточніть у менеджера по замовленням 067 470 87 21')
#
#
# # @user_private_router.message(F.text)
# # async def magic_filter_text(message: types.Message):
# #         await message.answer('Ваш текст поки-що не ідентифіковано')
#
# # @user_private_router.message(F.photo)
# # async def magic_filter_photo(message: types.Message):
# #         await message.answer('Це магічний фільтр зображень')
#
# @user_private_router.message(F.contact)
# async def get_contact(message: types.Message):
#         await message.answer(f'Контакт отримано')
#         await message.answer(str(message.contact))
#
# @user_private_router.message(F.location)
# async def get_location(message: types.Message):
#         await message.answer(f'Локацію отримано')
#         await message.answer(str(message.location))
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------
# from aiogram.utils.formatting import as_list, as_marked_section, Bold
#from kbds import reply, reply_2
#from kbds.reply_2 import get_keyboard
#---------------------------------------------------------------------
