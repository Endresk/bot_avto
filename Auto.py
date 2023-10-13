import asyncio
import html
import json
import logging
import math
import os
import re
import pandas as pd
import xlwings as xw
from itertools import chain
from threading import Thread

from aiogram import Bot
from numpy.random import default_rng
import aiohttp
import async_timeout
from cookie import headers, cookies
from pyquery import PyQuery
from time import sleep, time

from data import TOKEN

bot = Bot(token=TOKEN)

column_list = {
                0: 'A1', 1: 'B1', 2: 'C1', 3: 'D1', 4: 'E1', 5: 'F1', 6: 'G1', 7: 'H1', 8: 'I1', 9: 'J1', 10: 'K1',
                11: 'L1', 12: 'M1', 13: 'N1', 14: 'O1', 15: 'P1', 16: 'Q1', 17: 'R1', 18: 'S1', 19: 'T1', 20: 'U1',
                21: 'V1', 22: 'W1', 23: 'X1', 24: 'Y1'
            }


class Auto(Thread):
    def __init__(self, chat, result, UserID, brand, urlBrand):
        Thread.__init__(self)

        with open(f'JsonFiles/Parameters.json', "r") as read_file:
            parameters = json.load(read_file)

            self.minYear = parameters[f"{UserID}"]["minYear"]
            self.maxYear = parameters[f"{UserID}"]["maxYear"]
            self.DataReg = parameters[f"{UserID}"]["DataReg"]
            self.minPrice = parameters[f"{UserID}"]["minPrice"]
            self.maxPrice = parameters[f"{UserID}"]["maxPrice"]
            self.brand = brand
            self.urlBrand = urlBrand
            self.Result = result
            self.chat = chat

    def Result(self):
        if self.Result == 'file':
            asyncio.run(self.Model(self.brand, self.urlBrand))

    async def Model(self, brand, urlBrand):
        t1 = time()

        try:
            os.makedirs(f'Brands/{brand}')
        except FileExistsError:
            pass

        url = f"{urlBrand}/page1/?" \
              f"minprice={self.minPrice}&" \
              f"maxprice={self.maxPrice}&" \
              f"minyear={self.minYear}&" \
              f"maxyear={self.maxYear}&w=2&unsold=1"

        sem = asyncio.Semaphore(15)

        # Отключение прокси trust_env=True

        async with aiohttp.ClientSession(trust_env=True, headers=headers, cookies=cookies) as session:

            response = await session.get(url, headers=headers, cookies=cookies)

            pqHTML = PyQuery(await response.text(), parser="html")

            DictModelsMain, DictModelsOther, DictModelsResult = {}, {}, {}

            for i in pqHTML.find('.css-ofm6mg.exkrjba0 div div a').items():
                if not re.search(r'([^\s]+[+])', i.attr['href']):
                    DictModelsMain[i.text()] = i.attr['href']

            for i in pqHTML.find('.css-18clw5c.ehmqafe0 noscript a').items():
                if not re.search(r'([^\s]+[+])', i.attr['href']):
                    DictModelsOther[i.text()] = i.attr['href']

            DictModels = DictModelsMain | DictModelsOther

            DictModels = DictModels.values()

            ListModelsResult, ListModels = [], []
            for url in DictModels:
                ListModelsResult.append(await self.Page(url, session))

            ListEndModelsAll = [[
                "Ссылка",
                "Модель",
                "Год модели",
                "Цена",
                "Город"
            ]]

            if ListModelsResult:

                for i in list(filter(None, ListModelsResult)):
                    DictModelsResult.update(i)

                for i in DictModelsResult.values():
                    Url = i['url']
                    models = i['models']

                    if models:

                        if int(Url[1]) > 1:
                            ListModels.extend(i['models'])
                        else:
                            ListModels.append(i['models'])
                tasks = []
                Time = len(ListModels) / 15

                await bot.send_message(self.chat, f"Примерное время ожидания {Time} секунд")

                for m in ListModels:
                    tasks.append(asyncio.create_task(
                        self.UrlModelsSem(m[0], m[1], m[2], m[3], m[4], sem, session)))
                ListUrlModelsResult = await asyncio.gather(*tasks)
                print("Выполнил!")
                ListEndModels = list(filter(None, ListUrlModelsResult))
                ListEnd = list(chain(ListEndModelsAll, ListEndModels))

                df = pd.DataFrame(ListEnd)

                FileXLxs = f'Brands/{brand}/{brand}.xlsx'

                with xw.App(visible=False) as ap:

                    wb = ap.books.add()
                    ws = wb.sheets[0]
                    ws.name = brand

                    ws.range('A1').options(header=False, index=False, na_rep='').value = df

                    for column in df:
                        col = column_list[df.columns.get_loc(column)]
                        last_element = col.split('1')[0]

                    ws.range(f"$C1:${last_element}1").api.HorizontalAlignment = -4108

                    ws.range("C1").columns.autofit()

                    ws.range("A1").column_width = 35
                    ws.range("B1").column_width = 23
                    ws.range("D1").column_width = 13
                    ws.range("E1").column_width = 25

                    wb.save(path=FileXLxs)

        return ListEnd

    async def UrlModelsSem(self, UrlModel, Name, Age, City, Price, sem, session):
        async with sem:
            return await self.UrlModels(UrlModel, Name, Age, City, Price, session)

    async def UrlModels(self, UrlModel, Name, Age, City, Price, session):
        count = 0
        ListEndModels = []
        UrlModelCache = f"http://webcache.googleusercontent.com/search?q=cache:{UrlModel}&strip=0&vwsrc=1"
        while True:
            try:
                with async_timeout.timeout(15):
                    async with session.get(UrlModelCache, headers=headers,
                                           ssl_context=None,
                                           cookies=cookies) as ResponseModel:
                        response = await ResponseModel.read()

                        if ResponseModel.status != 429:
                            if ResponseModel.status != 404:
                                if ResponseModel.status == 200:

                                    NoJsonScript = self.AnalysisJsonScript(response)

                                    if re.search(r'о регистрации","data":', NoJsonScript):

                                        SplitNoJsonScript = NoJsonScript.split(
                                            'о регистрации","data":', 1)[1].split(".")[1].split(" по ")[0]

                                        if int(SplitNoJsonScript) >= 2010:
                                            ListEndModels.extend([UrlModel, Name, Age, Price, City])
                                    else:
                                        ListEndModels.extend(
                                            await self.UrlNoCache(UrlModel, Name, Age, City, Price, session))
                                    break
                            else:
                                ListEndModels.extend(
                                    await self.UrlNoCache(UrlModel, Name, Age, City, Price, session))
                                break
                        else:
                            count += 1
                            sleep(default_rng().uniform(3, 5))
                            if count > 3:
                                print("Спим 3 - 6")
                                sleep(default_rng().uniform(3, 6))

            except Exception as e:
                print(f"alert Models {UrlModel}", e)
                sleep(default_rng().uniform(1, 3))

        return ListEndModels

    @staticmethod
    def AnalysisJsonScript(response):
        pq = PyQuery(response, parser="html")

        PQStr = str(pq).replace("&lt;", "<") \
            .replace("&gt;", ">") \
            .replace("&quot;", '"') \
            .replace("&amp;", '&')

        PQ = PyQuery(html.unescape(PQStr).encode().decode('unicode-escape'), parser="html")
        JsonScript = PQ.find('script[data-drom-module="bull-page"]')
        NoJsonScript = str(JsonScript).replace("&lt;", "<").replace("&gt;", ">") \
            .replace("&quot;", '"') \
            .replace("&amp;", '&')

        return NoJsonScript

    async def UrlNoCache(self, UrlModel, Name, Age, City, Price, session):
        ListEndModels = []
        async with session.get(UrlModel,
                               headers=headers, cookies=cookies) as ResponseModelDRom:
            responseDRom = await ResponseModelDRom.read()
            NoJsonScriptDRom = self.AnalysisJsonScript(responseDRom)

            if re.search(r'о регистрации","data":', NoJsonScriptDRom):
                SplitNoJsonScriptDRom = NoJsonScriptDRom.split(
                    'о регистрации","data":', 1)[1].split(".")[1].split(" по ")[0]

                if int(SplitNoJsonScriptDRom) >= 2011:
                    ListEndModels.extend([UrlModel, Name, Age, Price, City])

        return ListEndModels

    async def Page(self, url, session):

        while True:
            try:
                with async_timeout.timeout(8):
                    async with session.get(url,
                                           headers=headers,
                                           ssl_context=None, cookies=cookies) as ResponsePage:

                        if ResponsePage.status == 200:
                            response = await ResponsePage.text()

                            pq = PyQuery(response, parser="html")
                            try:
                                SumPage = str(
                                    pq.find('#tabs div.css-1ksi09z').text()).replace('\xa0', '').split(" ")[0]
                            except:
                                SumPage = str(
                                    pq.find('#tabs div.css-1ksi09z').text()).split(" ")[0]

                            if SumPage:
                                SumPage = int(SumPage)
                                DictModel = {url.split("/")[4]: {'url': [url, SumPage]}}

                                listModels = [
                                    [
                                        i.attr['href'],
                                        str(i.find('.css-17lk78h.e3f4v4l2 span').text()).split(",")[0],
                                        int(str(i.find('.css-17lk78h.e3f4v4l2 span').text()).split(" ")[-1]),
                                        str(i.find('.css-1x4jcds.eotelyr0 span').text()),
                                        str(i.find('.css-46itwz.e162wx9x0 span').text()).replace("\xa0", " ")

                                    ] for i in pq.find('.css-1173kvb.eqhdpot0 '
                                                       'div.css-1nvf6xk.eqhdpot0:first '
                                                       'div '
                                                       'a.css-xb5nz8.e1huvdhj1').items()
                                    if
                                    i.find('div.css-1dkhqyq.e1f2m3x80 > div:nth-child(1) > div.css-z5srlr.e162wx9x0')
                                        .text() != 'снят с продажи'
                                ]

                                ListModelsResult = []

                                if len(listModels) == 1:
                                    listModels = listModels[0]
                                else:
                                    if SumPage > 20:

                                        QtyPage = math.ceil(SumPage / 20)

                                        for page in range(2, QtyPage + 1):
                                            urlPage = \
                                                f"{url.split('/?')[0]}/page{page}/?" \
                                                f"minprice={self.minPrice}&" \
                                                f"maxprice={self.maxPrice}&" \
                                                f"minyear={self.minYear}&" \
                                                f"maxyear={self.maxYear}&w=2&unsold=1"
                                            ListModelsResult.append(await self.Page_(urlPage, session))

                                listModels.extend(sum(ListModelsResult, []))

                                models = {
                                    'models': listModels
                                }

                                DictModel[url.split("/")[4]].update(models)

                                return DictModel
                            break
            except:
                print(f"alert Models {url}")

    @staticmethod
    async def Page_(urlPage, session):
        while True:
            try:
                with async_timeout.timeout(8):
                    async with session.get(urlPage,
                                           headers=headers,
                                           ssl_context=None, cookies=cookies) as ResponsePage:
                        if ResponsePage.status == 200:
                            response = await ResponsePage.text()
                            pq = PyQuery(response, parser="html")

                            listModels = [
                                [
                                    i.attr['href'],
                                    str(i.find('.css-17lk78h.e3f4v4l2 span').text()).split(",")[0],
                                    int(str(i.find('.css-17lk78h.e3f4v4l2 span').text()).split(" ")[-1]),
                                    str(i.find('.css-1x4jcds.eotelyr0 span').text()),
                                    str(i.find('.css-46itwz.e162wx9x0 span').text())
                                ] for i in pq.find('.css-1173kvb.eqhdpot0 '
                                                   'div.css-1nvf6xk.eqhdpot0:first '
                                                   'div a.css-xb5nz8.e1huvdhj1').items()
                                if i.find(
                                    'div.css-1dkhqyq.e1f2m3x80 > div:nth-child(1) > div.css-z5srlr.e162wx9x0').text()
                                   != 'снят с продажи'
                            ]
                            return listModels

            except:
                print(f"alert Model {urlPage}")
