from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
        *btns:str,
        placeholder: str = None,
        request_contact:int = None,
        request_location:int = None,
        sizes:tuple[int] = (2,),

):
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns,start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
                [
                    KeyboardButton(text='Меню'),
                    KeyboardButton(text='Про нас'),

                ],
                [
                    KeyboardButton(text='Варіанти доставки'),
                    KeyboardButton(text='Варіанти оплати'),
                ],
                [
                    KeyboardButton(text='Замовити'),
                ]

            ],
                resize_keyboard=True,
                input_field_placeholder='Що вас цікавить  ?'
)

del_kbd = ReplyKeyboardRemove()


start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
KeyboardButton(text="Меню"),
        KeyboardButton(text="Про нас"),
        KeyboardButton(text="Варіанти доставки"),
        KeyboardButton(text="Варіанти оплати")
)
start_kb2.adjust(2, 2)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text="Залишити відгук"))
start_kb3.row(KeyboardButton(text='Відправити номер ☎', request_contact= True),)
start_kb3.row(KeyboardButton(text='Відправити локацію 🚞', request_location= True),)
start_kb3.row(KeyboardButton(text='Створити опитання', request_poll=KeyboardButtonPollType()),)

test_kb = ReplyKeyboardMarkup(
    keyboard=[
                [
                    KeyboardButton(text='Створити опитання', request_poll=KeyboardButtonPollType()),

                ],
                [
                    KeyboardButton(text='Відправити номер ☎', request_contact= True),
                    KeyboardButton(text='Відправити локацію 🚞', request_location= True),
                ],
            ],
                resize_keyboard=True,
)
