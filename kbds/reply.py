from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

srart_kb = ReplyKeyboardMarkup(
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