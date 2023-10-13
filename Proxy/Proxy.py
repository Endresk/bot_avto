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


async def ProxyAll():
    AllListProxy = []
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(trust_env=True, headers=headers) as session:
        # -----
        # Сайт https://free-proxy-list.net/
        # -----
        try:
            async with session.get('https://free-proxy-list.net/', headers=headers) as ResponseProxy:
                response = await ResponseProxy.text()
                pq = PyQuery(response, parser="html")
                tbody = pq.find('#list > div > div.table-responsive > div > table > tbody')

                FPLProxy = [f"{td.find('td:lt(1)').text()}".split(" ")[0]
                            + ":" + f"{td.find('td:lt(1)').text()}".split(" ")[1]
                            for td in tbody.find('tr').items()]

            tasks = []
            for i in FPLProxy:
                tasks.append(asyncio.create_task(UrlProxy(i, session)))
            ProxyFPL = await asyncio.gather(*tasks, return_exceptions=True)

            FPLProxyAll = list(filter(None, ProxyFPL))
        except:
            FPLProxyAll = []

        # -----
        # Сайт https://fineproxy.org/wp-content/themes/fineproxy/proxy-list.php?0.8830517118035457
        # -----
        try:
            async with session.get(f'https://checkerproxy.net/api/archive/{datetime.today().strftime("%Y-%m-%d")}',
                                   headers=headers) as ResponseProxy:
                response = await ResponseProxy.json(content_type=None)
                FineProxy = [i["addr"] for i in response]

                tasks = []
                for proxy in FineProxy:
                    tasks.append(asyncio.create_task(UrlProxy(proxy, session)))
                FineProxyResult = await asyncio.gather(*tasks, return_exceptions=True)

                FineProxyAll = list(filter(None, FineProxyResult))
        except:
            FineProxyAll = []

        # -----
        # Сайт https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt
        # -----
        try:
            async with session.get('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
                                   headers=headers) as ResponseProxy:
                response = await ResponseProxy.text()
                GithubTheSpeedX = response.split("\n")
                tasks = []
                for proxy in GithubTheSpeedX:
                    tasks.append(asyncio.create_task(UrlProxy(proxy, session)))
                GithubTheSpeedXResult = await asyncio.gather(*tasks, return_exceptions=True)

                GithubTheSpeedXAll = list(filter(None, GithubTheSpeedXResult))
        except:
            GithubTheSpeedXAll = []

        # -----
        # Сайт https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt
        # -----
        try:
            cookiesGhostEaLth = {
                '_gcl_au': '1.1.701894776.1678302461',
                '_ga': 'GA1.2.1018492779.1678302461',
                '_gid': 'GA1.2.695390805.1678302461',
                'gs_co': '1678303360347',
                '_gat_gtag_UA_139521328_3': '1',
            }

            headersGhostEaLth = {
                'authority': 'ghostealth.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9'
                                 '.eyJzdWIiOiIxODE1MTQwZGFmMDc4NjNkMTk0MWJlMDlhYzExMjk3ODcxZDlmIn0.UFDEOTCDHbbGjH'
                                 '-x961hPcUDOlSmuKVg4R-dwvAcvSY',
                'referer': 'https://ghostealth.com/proxy-scraper',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/110.0.0.0 Safari/537.36',
            }

            async with session.get('https://ghostealth.com/api/v1.0/dev/tools/proxy-scraper/proxies/extended',
                                   cookies=cookiesGhostEaLth, headers=headersGhostEaLth) as ResponseProxy:
                response = await ResponseProxy.json(content_type=None)

                tasks = []
                for proxy in [i['ip'] for i in response['result']]:
                    tasks.append(asyncio.create_task(UrlProxy(proxy, session)))
                GithubTheSpeedXResult = await asyncio.gather(*tasks, return_exceptions=True)

                GhostEalThAll = list(filter(None, GithubTheSpeedXResult))
        except:
            GhostEalThAll = []

        # -----
        # Сайт https://freeproxyupdate.com/free-proxy-list-txt-download
        # -----
        try:
            async with session.get('https://freeproxyupdate.com/free-proxy-list-txt-download',
                                   headers=headers) as ResponseProxy:
                responseProxy = await ResponseProxy.text()
                pq = PyQuery(responseProxy, parser="html")

                UrlNumCountry = [[f"https://freeproxyupdate.com{i.find('td > a').attr['href']}",
                                  i.find('td:nth-child(2)').text()] for i in
                                 pq.find('#main-content > table:nth-child(8) > tbody > tr').items()
                                 if int(i.find('td:nth-child(2)').text()) > 0]
                tasks = []
                for i in UrlNumCountry:
                    tasks.append(asyncio.create_task(UrlPageFreeProxyUpdate(i, session, sem)))
                FreeProxyUpdateResult = await asyncio.gather(*tasks, return_exceptions=True)

                tasksCheck = []
                for i in sum(FreeProxyUpdateResult, []):
                    if i[1] == 'http':
                        tasksCheck.append(asyncio.create_task(FreeProxyUpdateCheck(i[0], i[1], session)))
                DictGeoNodeResultAll = await asyncio.gather(*tasksCheck, return_exceptions=True)

                DictGeoNodeAll = list(filter(None, DictGeoNodeResultAll))
        except:
            DictGeoNodeAll = []

    AllListProxy = list(set(list(chain(FPLProxyAll, FineProxyAll, GithubTheSpeedXAll, GhostEalThAll, DictGeoNodeAll))))
    print(AllListProxy)
    with open('AllListProxy.json', 'w') as f:
        json.dump(AllListProxy, f)


async def UrlPageFreeProxyUpdate(i, session, sem):
    async with sem:
        # Функция перебора стран первая страница и единственная
        if int(i[1]) <= 50:
            ListCountry = await UrlPageFreeProxyUpdateAllPage(i[0], session)

        # Функция перебора стран все страницы
        else:

            tasks = []
            for j in range(1, math.ceil(int(i[1]) / 50) + 1):

                tasks.append(asyncio.create_task(
                    UrlPageFreeProxyUpdateAllPage(f"{i[0]}/page-{j}", session)))
            ListCountry = await asyncio.gather(*tasks, return_exceptions=True)
            ListCountry = ListCountry[0]

        return ListCountry


async def UrlPageFreeProxyUpdateAllPage(i, session):
    ListCountry = []
    try:
        async with session.get(i, headers=headers) as ResponseCountry:
            responseCountry = await ResponseCountry.text()

            pqCountry = PyQuery(responseCountry, parser="html")

            for j in pqCountry.find("#main-content > table.list-proxy > tbody  > tr").items():
                address = f"{j.find('td:nth-child(1)').text()}:{j.find('td:nth-child(2)').text()}"

                if re.search(r'([^\s]+[.][^\s]+[.][^\s]+[.]+[^\s]+[:]+[^\s])', address):
                    ListCountry.append([address, j.find('td:nth-child(5) > a').text()])
    except:
        ListCountry = []

    return ListCountry


async def FreeProxyUpdateCheck(address, protocol, session):
    try:
        async with session.get('https://auto.drom.ru/audi/a3/?minyear=2000&maxyear=2009&w=2&unsold=1',
                               proxy=f"{protocol}://{address}",
                               timeout=15,
                               headers=headers,
                               ssl_context=None) as response:
            if response.status == 200:
                return f"{protocol}://{address}"

    except:
        await asyncio.sleep(0)


async def UrlProxy(i, session):
    try:
        async with session.get('https://auto.drom.ru/audi/a3/?minyear=2000&maxyear=2009&w=2&unsold=1',
                               proxy=f"http://{i}", timeout=1, headers=headers, ssl_context=None) as response:
            if response.status == 200:
                return f"http://{i}"

    except:
        await asyncio.sleep(0)

# Protocol = [
#           'http',
#           'https',
#           'SOCKS4',
#           'SOCKS5'
#       ]
