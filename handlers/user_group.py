from string import punctuation

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from const import COMMANDS_LIST, RESTRICTED_WORDS
from filters.chat_types import ChatTypefilter

user_group_router = Router()
user_group_router.message.filter(ChatTypefilter(['group', 'supergroup']))


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
# @user_group_router.edited_message()
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    print(message.text.lower().split())
    if RESTRICTED_WORDS.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, "
                             f"\n ваше повідомлення було видалене \n "
                             f"у зв'язку з використанням заборонених слів. \n"
                             f"Плекайте порядок у чаті.")
        await message.delete()
        # await message.chat.ban(message.from_user.id)


