from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from const import COMMANDS_LIST
from filters.chat_types import ChatTypefilter

from kbds import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypefilter(['private']))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"Доброго дня {message.from_user.full_name} - я віртуальний помічник ", reply_markup=reply.srart_kb)
@user_private_router.message(or_f(Command('menu'), (F.text.lower().contains('меню'))))
async def menu_comands(message: types.Message):
        await message.answer('Тут буде меню',reply_markup=reply.del_kbd)

@user_private_router.message(Command('cl'))
async def commands_list(message: types.Message):
        await message.answer(COMMANDS_LIST)


@user_private_router.message((F.text.lower().contains('про нас')) | (F.text.lower().contains('знайти')))
@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
        await message.answer('Про нас')

@user_private_router.message((F.text.lower().contains('оплат')) | (F.text.lower() == 'варіанти оплати') | (F.text.lower().contains('заплат')))
@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
        await message.answer('З приводу оплати вам розповість менеджер з продажу 067 470 87 21')


@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варіанти доставки'))
async def magic_filter_text_contains(message: types.Message):
        await message.answer('З питань доставки уточніть у логіста 067 470 87 21')

@user_private_router.message((F.text.lower() == 'привіт') |
                             (F.text.lower() == 'доброго дня') |
                             (F.text.lower() == 'добрий день'))
async def magic_filter_text_greeting(message: types.Message):
        await message.answer(f'Вітаємо Вас \n{message.from_user.first_name}')

@user_private_router.message( (F.text.lower().contains('замовити')) | (F.text.lower().contains('замовлення')) )
async def magic_filter_text_order(message: types.Message):
        await message.answer('З приводу замовлень уточніть у менеджера по замовленням 067 470 87 21')


@user_private_router.message(F.text)
async def magic_filter_text(message: types.Message):
        await message.answer('Ваш текст поки-що не ідентифіковано')

@user_private_router.message(F.photo)
async def magic_filter_photo(message: types.Message):
        await message.answer('Це магічний фільтр зображень')


