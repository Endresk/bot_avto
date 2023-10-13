import json

from aiogram import types

markup_main = [
    [
        types.KeyboardButton(text='Дром'),
        types.KeyboardButton(text='Настройки')
    ]
]
markup_main = types.ReplyKeyboardMarkup(keyboard=markup_main, resize_keyboard=True)
