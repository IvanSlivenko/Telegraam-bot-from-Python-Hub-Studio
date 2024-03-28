from string import punctuation

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from const import COMMANDS_LIST, RESTRICTED_WORDS

user_group_router = Router()

restricted_words = {
                    'кабан',
                    'хомяк',
                    'вихухоль'
                    }

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    # if restricted_words.intersection(message.text.lower().split()):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, плекайте порядок у чаті")
        await message.delete()
        # await message.chat.ban(message.from_user.id)


