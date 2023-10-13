import json
import logging
from time import sleep

import aiohttp
from aiogram import Bot, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hpre, text, hlink
from pyquery import PyQuery
from tabulate import tabulate
from Auto import Auto
from cookie import headers, cookies
from data import TOKEN
from keyboards.KeyboardResult import InlineKeyboard_result
from main import DictDefault

bot = Bot(token=TOKEN)
router = Router()


class Form_add(StatesGroup):
    page = State()
    Dict = State()
    result = State()


@router.message(Text(text='Дром', ignore_case=True))
async def cmd_brand(message: types.Message):
    try:
        with open('JsonFiles/InputPass.json', "r") as read_file:
            DictInputPass = json.load(read_file)

        if message.from_user.username in DictInputPass.keys():
            await message.answer("Выберите метод получения результата поиска:", reply_markup=InlineKeyboard_result)
    except:
        pass


@router.callback_query(Text(startswith="result_"))
async def callbacks_next(callback: types.CallbackQuery, state: FSMContext):
    result = callback.data.replace('result_', '')

    with open('JsonFiles/Parameters.json', "r") as read_file:
        DictUsers = json.load(read_file)

    UserID = str(callback.from_user.id)

    if UserID not in DictUsers:
        with open(f'JsonFiles/Parameters.json', 'w') as f:
            DictUsers[UserID] = DictDefault
            json.dump(DictUsers, f)
    try:
        with open('JsonFiles/Brands.json', 'r') as file:
            DictBrand = json.load(file)
            DictBrand = list(sorted(DictBrand.keys()))
            LenDict = len(DictBrand)
            DictIndex = {}
            for i in range(0, LenDict, 20):
                DictIndex[i] = DictBrand[i:i + 20]

            await state.update_data(page=0)
            await state.update_data(Dict=DictIndex)
            await state.update_data(result=result)

            DictUserParameters = DictUsers[UserID]

            data_couple = tabulate([["Цена от", DictUserParameters['minPrice'],
                                     "Год от", DictUserParameters['minYear']
                                     ],
                                    ["Цена до", DictUserParameters['maxPrice'],
                                     "Год до", DictUserParameters['maxYear']]
                                    ],
                                   tablefmt='simple',
                                   showindex=False,
                                   colalign=("right", "left", "left", "left"))

            await callback.message.edit_text(text(hpre(data_couple),
                                                  "\nВыберите бренд"),
                                             parse_mode="HTML",
                                             reply_markup=await Pagination(state))

    except:
        DictBrand = {}
        async with aiohttp.ClientSession(trust_env=True,
                                         headers=headers, cookies=cookies) as session:
            async with session.get('https://auto.drom.ru/',
                                   headers=headers, ssl_context=None, cookies=cookies) as ResponseModel:
                pqHTML = PyQuery(await ResponseModel.text(), parser="html")
                OneDivPQ = pqHTML.find('div > div.css-18clw5c.ehmqafe0')

                for i in OneDivPQ.find('div > div > div > a').items():
                    DictBrand[i.text()] = i.attr['href']

                for i in OneDivPQ.find("noscript a").items():
                    Url = i.attr['href']
                    if str(Url).split("/")[-2] != 'other':
                        DictBrand[i.text()] = Url
        with open('JsonFiles/Brands.json', 'w') as f:
            json.dump(DictBrand, f)


async def Pagination(state):
    builder = InlineKeyboardBuilder()

    data = await state.get_data()

    page = int(data['page'])
    DictIndex = data['Dict']

    for i in DictIndex[page]:
        builder.add(types.InlineKeyboardButton(
            text=i,
            callback_data=f"brand_{i}"))

    if page != 0 and int(next(reversed(DictIndex.keys()))) != page:
        builder.row(types.InlineKeyboardButton(text='Назад', callback_data='back'))
        builder.add(types.InlineKeyboardButton(text='Далее', callback_data='next'))
        builder.adjust(4)
    elif page == 0:
        builder.row(types.InlineKeyboardButton(text='Далее', callback_data='next'))
        builder.adjust(4)
    else:
        builder.row(types.InlineKeyboardButton(text='Назад', callback_data='back'))

    return builder.as_markup()


@router.callback_query(Text(startswith="brand_"))
async def callbacks_next(callback: types.CallbackQuery, state: FSMContext):
    brand = callback.data.replace('brand_', '')
    data = await state.get_data()
    result = data['result']

    with open('JsonFiles/Brands.json', 'r') as file:
        DictBrand = json.load(file)
    await callback.message.edit_text(f"Выбран бренд «{brand}»"
                                     "\n\nЗагружаю...")
    await callback.answer()

    if result == 'file':
        h = await Auto(callback.from_user.id, result, callback.from_user.id, brand,
                       DictBrand[brand]).Model(brand, DictBrand[brand])
        print(h)
        await callback.message.answer_document(FSInputFile(f'Brands/{brand}/{brand}.xlsx'))
    else:
        ListBrand = await Auto(callback.from_user.id, result, callback.from_user.id, brand,
                               DictBrand[brand]).Model(brand, DictBrand[brand])

        count = 0

        List, Headers = [], []

        Len = int(len(ListBrand))

        print("Len", Len)

        for i in ListBrand:
            if count == 0:
                List.append([f'{i[1]} | {i[2]} | {i[3]} | {i[4]}'])
                count += 1
            else:
                Url = i[0]
                List.append([hlink(f'{i[1]} |  {i[2]} | {i[3]} | {i[4]}', f"{Url}")])

        if Len > 93:
            for i in list(func_chunks_generators(List, 93)):
                print(i)
                print(len(i))
                data_couple = tabulate(i,
                                       tablefmt="plain",
                                       showindex=False)
                await callback.message.answer(text(data_couple), parse_mode="HTML",
                                              disable_web_page_preview=True)
        else:
            data_couple = tabulate(List,
                                   tablefmt="plain",
                                   showindex=False)
            await callback.message.answer(text(data_couple), parse_mode="HTML",
                                          disable_web_page_preview=True)


def func_chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


@router.callback_query(Text(startswith="next"))
async def callbacks_next(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(page=int(data['page']) + 20)
    await callback.message.edit_text("Выберите бренд", reply_markup=await Pagination(state))
    await callback.answer()


@router.callback_query(Text(startswith="back"))
async def callbacks_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.update_data(page=int(data['page']) - 20)
    await callback.message.edit_text("Выберите бренд", reply_markup=await Pagination(state))
    await callback.answer()
