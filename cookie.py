import random

from fake_useragent import UserAgent

useragent = UserAgent()

cookies = {
    'ring': '90016f88100fabcd636af51648342612',
    '_ym_uid': '1672038408430277260',
    '_ym_d': '1672038408',
    'cookie_cityid': '16',
    'cookie_regionid': '63',
    'dr_df': '1',
    'apple-pay-available': '0',
    'google-pay-available': '1',
    'PHPSESSID': 'a1e47e9969de989b3aaef45451671de9',
    'last_search_auto_compatibility': 'model%3DKia%2BSportage%26autoPartsGeneration%3D4%26autoPartsVolume%3D2000'
                                      '%26autoPartsFuel%3Dgasoline',
    'city': '827',
    'my_geo': '63',
    'spare_parts_bulls_counter': '22',
    '_ga_MYQZ43FGYD': 'GS1.1.1675670848.6.1.1675672052.0.0.0',
    '_ga_C9HGECLFK7': 'GS1.1.1675670848.6.1.1675672052.0.0.0',
    '_gcl_au': '1.1.1968856211.1675920486',
    'tmr_lvid': 'af60d9287f8a7defb5d2f0ff7a9e12d4',
    'tmr_lvidTS': '1675920486270',
    'last_search_wheel_size_metrical': 'sectionWidth%3D235%26sectionHeight%3D45%26wheelDiameter%3D18',
    '_ga_D5S0HQT12H': 'GS1.1.1675937340.3.0.1675937340.0.0.0',
    '_ga_W0TFWNSLJ7': 'GS1.1.1675937340.9.0.1675937340.0.0.0',
    '_ga': 'GA1.2.1945041783.1672038407',
    '_gid': 'GA1.2.629886603.1677045255',
    'k6W': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImRMQ2MxZUFvdV9kZkwteFVWMmdiWHlUM0JnWnAyYVNFSS00UGdIVzlkNEkiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE2NzcxNDEzMjUsImtpZCI6ImRMQ2MxZUFvdV9kZkwteFVWMmdiWHlUM0JnWnAyYVNFSS00UGdIVzlkNEkiLCJwcm9qZWN0IjoiZHJvbSIsInN1YiI6InI6OTAwMTZmODgxMDBmYWJjZDYzNmFmNTE2NDgzNDI2MTIifQ.rfax3Aeu10DsVo7PxUFj4mJEPSiwUSnjxUQYaGtA86NOkud1uBthB170FDutCB-gCNCKRJjx5FWElpAJUsCTe8TVKhbOlNmJ_Vu3KgvJDqaA0CM3EskpMsX78gDYGg74yRSGYQdgZJH8P0XuOz2kJP1AucVdLsyr-yzF0f_lAe0',
    'segSession': 'ImY1NjQ1Mzk4NWI1YzI4MDg3NWNhY2E4YjAyYzVkMjhibm90QXV0aDkwMDE2Zjg4MTAwZmFiY2Q2MzZhZjUxNjQ4MzQyNjEyIl9jM2FkM2M4ZjJiNmU2MmFiMzc3NjQ2NTA0M2M4ZjUxYw',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://auto.drom.ru/audi/a6_allroad_quattro/page5/?minyear=2000&maxyear=2009&w=2&unsold=1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': useragent.chrome,
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


