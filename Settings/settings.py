import json
import re
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Text
from aiogram.utils.markdown import text, hbold
from data import TOKEN
from keyboards.KeyboardSettings import InlineKeyboard_settings
from keyboards.KeyboardMain import markup_main

bot = Bot(token=TOKEN)
router = Router()


class Form_add(StatesGroup):
    parameter = State()


@router.message(Text(text='Настройки'))
async def cmd_settings(message: types.Message):
    with open('JsonFiles/InputPass.json', "r") as ReadFile:
        DictInputPass = json.load(ReadFile)

    if message.from_user.username in DictInputPass.keys():
        UserID = message.from_user.id
        with open(f'JsonFiles/Parameters.json', "r") as ReadFile:
            parameters = json.load(ReadFile)

        minYear = parameters[f"{UserID}"]["minYear"]
        maxYear = parameters[f"{UserID}"]["maxYear"]
        DataReg = parameters[f"{UserID}"]["DataReg"]
        minPrice = parameters[f"{UserID}"]["minPrice"]
        maxPrice = parameters[f"{UserID}"]["maxPrice"]

        await message.answer(text(f"Параметры поиска"
                                  f"\n\nЦена от: {hbold(minPrice)}"
                                  f"\nЦена до: {hbold(maxPrice)}"
                                  f"\nГод от: {hbold(minYear)}"
                                  f"\nГод до: {hbold(maxYear)}"
                                  f"\nДата первой регистрации от: {hbold(DataReg)}"),
                             parse_mode="html",
                             reply_markup=InlineKeyboard_settings)


@router.callback_query(Text(startswith="edit_"))
async def callbacks_edit(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await state.update_data(parameter=action)

    if action == "minYear":
        EditText = "Изменить «Год ОТ»"
    elif action == "maxYear":
        EditText = "Изменить «Год ДО»"
    elif action == "minPrice":
        EditText = "Изменить «Цена ОТ»"
    elif action == "maxPrice":
        EditText = "Изменить «Цена ДО»"
    else:
        EditText = "Изменить «Дата первой регистрации»"

    if action in ["minYear", "maxYear", "DataReg"]:
        InputText = "год"
        code = 1
    else:
        InputText = "цену"
        code = 2
    await callback.message.answer(f"Вы выбрали: {EditText}"
                                  f"\n\nОк, введите {InputText}")

    with open(f'JsonFiles/Parameters.json', "r") as ReadFile:
        Parameters = json.load(ReadFile)
    DictValue = Parameters[f"{callback.from_user.id}"]
    DictValue |= {"code": code}
    Parameters |= {f"{callback.from_user.id}": DictValue}

    with open(f'JsonFiles/Parameters.json', "w") as WriteFile:
        json.dump(Parameters, WriteFile)

    await callback.answer()


@router.message(F.text.regexp(r'[0-9]+$'))
async def cmd_edit(message: types.Message, state: FSMContext):
    with open('JsonFiles/InputPass.json', "r") as ReadFile:
        DictInputPass = json.load(ReadFile)

    if message.from_user.username in DictInputPass.keys():

        data = await state.get_data()
        parameter = data['parameter']

        with open(f'JsonFiles/Parameters.json', "r") as ReadFile:
            Parameters = json.load(ReadFile)
        DictValue = Parameters[f"{message.from_user.id}"]
        Code = DictValue["code"]

        if parameter in ["minYear", "maxYear", "DataReg"] and Code == 1:
            if re.findall(r'20[0-9]+$', message.text):
                await Edit(DictValue, parameter, Parameters, message)
        else:
            await Edit(DictValue, parameter, Parameters, message)


async def Edit(DictValue, parameter, Parameters, message):
    DictValue |= {"code": 0, f"{parameter}": int(message.text)}
    Parameters |= {f"{message.from_user.id}": DictValue}

    with open(f'JsonFiles/Parameters.json', "w") as WriteFile:
        json.dump(Parameters, WriteFile)

    minYear = DictValue["minYear"]
    maxYear = DictValue["maxYear"]
    DataReg = DictValue["DataReg"]
    minPrice = DictValue["minPrice"]
    maxPrice = DictValue["maxPrice"]

    await message.answer("Параметр поиска изменен!"
                         f"\n\nЦена от: {hbold(minPrice)}"
                         f"\nЦена до: {hbold(maxPrice)}"
                         f"\nГод от: {hbold(minYear)}"
                         f"\nГод до: {hbold(maxYear)}"
                         f"\nДата первой регистрации: {hbold(DataReg)}",
                         parse_mode="html",
                         reply_markup=markup_main
                         )
