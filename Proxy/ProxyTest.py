import asyncio
import json
import math
import random
import re
from datetime import datetime
from itertools import chain
from time import sleep, time

import aiohttp
from pyquery import PyQuery

from cookie import headers


async def ProxyTest():
    async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        try:
            async with session.get('https://www.freeproxy-list.ru/proxy-list/1', headers=headers) as Response:
                response = await Response.text()
                pq = PyQuery(response, parser="html")
                noindex = pq.find(
                    '#main-cont > div > div.row > div.col-md-10 > div.content1:nth-child(9) > noindex > a')

                ListUrlPort = [{i.attr['href']: i.text()} for i in noindex.items()]
                tasks = []
            for i in ListUrlPort:
                # await ListProxy(list(i.keys())[0], list(i.values())[0], session)
                tasks.append(asyncio.create_task(ListProxy(list(i.keys())[0], list(i.values())[0], session)))
            FreeProxyList = await asyncio.gather(*tasks, return_exceptions=True)

            print(sum(FreeProxyList, []))

            tasksUrl = []
            for proxy in sum(FreeProxyList, []):
                tasksUrl.append(asyncio.create_task(UrlProxy(proxy, session)))
            FreeProxyListResult = await asyncio.gather(*tasksUrl, return_exceptions=True)

            print(FreeProxyListResult)

            sleep(5000)

        except:
            print("error FreeProxyList")
            FreeProxyAll = []
        print("FreeProxyList", FreeProxyList)


async def ListProxy(PartUrl, port, session):
    ListAddressAll, FreeProxyList = [], []

    async with session.get(f"https://www.freeproxy-list.ru{PartUrl}/proxy-list/1",
                           headers=headers) as ResponseUrl:
        responseUrl = await ResponseUrl.text()
        pq = PyQuery(responseUrl, parser="html")
        RTH = pq.find('#main-cont > div > div.row > div.col-md-10 > div.table.container > div.row.tr.hover')
        pageHtml = pq.find('#main-cont > div > div.row > div.col-md-10 > div.page > noindex:last > a')
        try:
            page = int(str(pageHtml.attr['href']).split("/")[-1])
        except:
            page = 2

        if len(pageHtml) == 0:
            pageHtml = pq.find('#main-cont > div > div.row > div.col-md-10 > div.page > noindex').eq(-2)
            page = int(str(pageHtml.find('a').attr['href']).split("/")[-1]) + 1

        for i in RTH.items():
            ip = i.find('div.col-md-2.td:nth-child(1)').text()
            ListAddressAll.append(f'{ip}:{port}')

    if page == 2:
        pass
    else:
        tasks = []
        for i in range(2, int(page) + 1):
            tasks.append(asyncio.create_task(AllListProxy(i, PartUrl, port, session)))
        FreeProxyList = await asyncio.gather(*tasks, return_exceptions=True)

        ListAddressAll.extend(sum(FreeProxyList, []))

    return ListAddressAll


async def AllListProxy(page, PartUrl, port, session):
    ListAddress = []
    async with session.get(f"https://www.freeproxy-list.ru{PartUrl}/proxy-list/{page}",
                           headers=headers) as ResponseUrl:
        responseUrl = await ResponseUrl.text()
        pq = PyQuery(responseUrl, parser="html")
        RTH = pq.find('#main-cont > div > div.row > div.col-md-10 > div.table.container > div.row.tr.hover')
        for i in RTH.items():
            ip = i.find('div.col-md-2.td:nth-child(1)').text()
            ListAddress.append(f'{ip}:{port}')

    return ListAddress


async def UrlProxy(i, session):
    try:
        async with session.get('https://auto.drom.ru/audi/a3/?minyear=2000&maxyear=2009&w=2&unsold=1',
                               proxy=f"http://{i}", timeout=5, headers=headers, ssl_context=None) as response:
            if response.status == 200:
                return f"http://{i}"

    except:
        await asyncio.sleep(0)