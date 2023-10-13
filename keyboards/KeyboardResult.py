from aiogram import types

inline_keyboard = [
    [
        types.InlineKeyboardButton(text='В файл', callback_data="result_file"),
        types.InlineKeyboardButton(text='В бота', callback_data="result_bot"),
    ]
]
InlineKeyboard_result = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=False)
