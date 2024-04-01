from string import punctuation

from aiogram import F, Bot, types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from const import COMMANDS_LIST, RESTRICTED_WORDS
from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))
user_group_router.edited_message.filter(ChatTypeFilter(['group', 'supergroup']))

@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)

    # print('1', admins_list)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]

    # print('2 ', admins_list)
    # print('current_user_id',message.from_user.id)
    # print('bot.my_admins_list', bot.my_admins_list)

    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        # await message.answer('Ваш статус : administrator')
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))
# @user_group_router.edited_message()
@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    # print(message.text.lower().split())
    if RESTRICTED_WORDS.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, "
                             f"\n ваше повідомлення було видалене \n "
                             f"у зв'язку з використанням заборонених слів. \n"
                             f"Плекайте порядок у чаті.")
        await message.delete()
        # await message.chat.ban(message.from_user.id)


