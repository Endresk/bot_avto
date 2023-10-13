import asyncio
import json
import logging
import os
import sys
import nest_asyncio
from aiogram import Bot, types, Router, Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, Text
from aiogram.fsm.strategy import FSMStrategy
from Settings import settings
from Result import ResultBrand
from keyboards.KeyboardMain import markup_main
from data import TOKEN, PASSWORD

bot = Bot(token=TOKEN)
router = Router()


DictDefault = {
  "minYear": 2000,
  "maxYear": 2009,
  "minDataReg": 2011,
  "maxDataReg": 2012,
  "minPrice": 0,
  "maxPrice": 1000000,
  "code": 0
}


try:
    os.makedirs(f'Brands')
except FileExistsError:
    pass

try:
    os.makedirs(f'JsonFiles')
except FileExistsError:
    pass

try:
    with open('JsonFiles/InputPass.json', "r") as readFile:
        InputPass = json.load(readFile)
except:
    with open('JsonFiles/InputPass.json', 'w') as WriteFile:
        json.dump({}, WriteFile)

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", )


@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    try:
        with open('JsonFiles/InputPass.json', "r") as read_file:
            DictInputPass = json.load(read_file)

            if message.from_user.username in DictInputPass.keys():
                await message.answer(f'Приветствую тебя {message.from_user.username}', reply_markup=markup_main)
            else:
                await message.answer(f'Приветствую тебя {message.from_user.username}!'
                                     f'\nВведите пароль для дальнейшего использования:')
    except:
        with open('JsonFiles/InputPass.json', 'w') as f:
            json.dump({}, f)
        await message.answer(f'Приветствую тебя {message.from_user.username}!'
                             f'\nВведите пароль для дальнейшего использования:')


@router.message(Text(text=PASSWORD, ignore_case=True))
async def cmd_Pass(message: types.Message):
    try:
        with open('JsonFiles/InputPass.json', "r") as read_file:
            DictInputPass = json.load(read_file)

            if message.from_user.username not in DictInputPass.keys():
                DictInputPass[message.from_user.username] = PASSWORD

                await message.answer(f'{message.from_user.username} вы ввели верный пароль. \nДоступ разрешен!',
                                     reply_markup=markup_main)

                with open('JsonFiles/InputPass.json', 'w') as f:
                    json.dump(DictInputPass, f)

                with open(f'JsonFiles/Parameters.json', "r") as ReadFile:
                    DictUsers = json.load(ReadFile)

                DictUsers[message.from_user.id] = DictDefault

                with open(f'JsonFiles/Parameters.json', 'w') as f:
                    json.dump(DictUsers, f)
    except Exception as e:
        logging.critical(e, exc_info=True)


async def main():
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    dp.include_router(router)
    dp.include_router(settings.router)
    dp.include_router(ResultBrand.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
