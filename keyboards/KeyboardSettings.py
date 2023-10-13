from aiogram import types

inline_keyboard = [
    [
        types.InlineKeyboardButton(text='Изменить «Цена ОТ»', callback_data="edit_minPrice"),
        types.InlineKeyboardButton(text='Изменить «Цена ДО»', callback_data="edit_maxPrice"),
    ],
    [
        types.InlineKeyboardButton(text='Изменить «Год ОТ»', callback_data="edit_minYear"),
        types.InlineKeyboardButton(text='Изменить «Год ДО»', callback_data="edit_maxYear"),
    ],
    [
        types.InlineKeyboardButton(text='Изменить «Дата первой регистрации»', callback_data="edit_DataReg")
    ]

]
InlineKeyboard_settings = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard,
                                                     resize_keyboard=True,
                                                     one_time_keyboard=False)
