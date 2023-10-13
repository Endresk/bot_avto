import asyncio
import json
import random
import re
from time import sleep
import html
import aiohttp
import async_timeout
from numpy.random import default_rng
from pyquery import PyQuery

from cookie import headers, cookies


async def Models():
    with open(f'Brands/Audi/Models/UrlsModels.json', 'r') as f:
        Json = json.load(f)

    ListEndModels, ListModels = [], []

    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        for i in Json.values():

            Url = i['url']
            models = i['models']

            if models:

                if int(Url[1]) > 1:
                    ListModels.extend(i['models'])
                else:
                    ListModels.append(i['models'])

        tasks = []
        count = 0

        for m in ListModels:
            tasks.append(asyncio.create_task(UrlModelsSem(m[0], m[1], m[2], m[3], sem, session, count)))

        ListEndModels = await asyncio.gather(*tasks)

        ListEndModels = list(filter(None, ListEndModels))

        print(count)

        json.dump(ListEndModels, open(
            f"Brands/Audi/Models/ListEndModelsAll.json", "w"))
        print(ListEndModels)

        sleep(500)


async def UrlModelsSem(UrlModel, Name, Age, City, sem, session, count):
    async with sem:
        return await UrlModels(UrlModel, Name, Age, City, session, count)


async def UrlModels(UrlModel, Name, Age, City, session, count):

    ListEndModels = []

    UrlModelCache = f"http://webcache.googleusercontent.com/search?q=cache:{UrlModel}&strip=0&vwsrc=1"
    print(UrlModel, Age, UrlModelCache)

    while True:

        try:
            with async_timeout.timeout(15):
                async with session.get(UrlModelCache,
                                       headers=headers, cookies=cookies) as ResponseModel:
                    response = await ResponseModel.read()

                    if ResponseModel.status != 429:
                        if ResponseModel.status != 404:
                            if ResponseModel.status == 200:

                                NoJsonScript = AnalysisJsonScript(response)

                                if re.search(r'о регистрации","data":', NoJsonScript):

                                    SplitNoJsonScript = NoJsonScript.split(
                                        'о регистрации","data":', 1)[1].split(".")[1].split(" по ")[0]

                                    if int(SplitNoJsonScript) == 2011:
                                        DateReg = int(SplitNoJsonScript)
                                        ListEndModels.extend([UrlModel, Name, Age, DateReg, City])
                                        print(SplitNoJsonScript)

                                else:
                                    count += 1

                                    ListEndModels.extend(await UrlNoCache(UrlModel, Name, Age, City, session))
                                break
                        else:
                            count += 1
                            ListEndModels.extend(await UrlNoCache(UrlModel, Name, Age, City, session))
                            break
                    else:
                        count += 1
                        sleep(default_rng().uniform(3, 5))
                        if count > 3:
                            print("Спим 3 - 5")
                            sleep(default_rng().uniform(3, 5))
        except:
            print(f"alert Models {UrlModel}")
            sleep(default_rng().uniform(1, 3))

    return ListEndModels


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


async def UrlNoCache(UrlModel, Name, Age, City, session):
    ListEndModels = []
    async with session.get(UrlModel,
                           headers=headers, cookies=cookies) as ResponseModelDRom:
        responseDRom = await ResponseModelDRom.read()
        NoJsonScriptDRom = AnalysisJsonScript(responseDRom)

        if re.search(r'о регистрации","data":', NoJsonScriptDRom):
            SplitNoJsonScriptDRom = NoJsonScriptDRom.split(
                'о регистрации","data":', 1)[1].split(".")[1].split(" по ")[0]

            if int(SplitNoJsonScriptDRom) == 2011:
                DateReg = int(SplitNoJsonScriptDRom)
                ListEndModels.extend([UrlModel, Name, Age, DateReg, City])
                print(SplitNoJsonScriptDRom)

    return ListEndModels
