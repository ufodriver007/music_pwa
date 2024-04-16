import os
import asyncio
import aiohttp
import requests
from vkpymusic import TokenReceiver, Service, ServiceAsync
import json
import time


def get_new_vk_token():
    """
    Use vk_login and vk_password. Write token to self config(venv/lib/python3.11/site-packages/vkpymusic/config_vk.ini)
    :return:
    """
    login = 'vk_login'
    password = 'vk_password'

    token_receiver = TokenReceiver(login, password)

    if token_receiver.auth():
        token_receiver.get_token()
        token_receiver.save_to_config()


def convert_song_duration(seconds: int) -> str:
    """
    Convert song duration(in seconds) to duration('xx:xx')
    :param seconds:
    :return:
    """
    mins = seconds // 60
    secs = seconds % 60
    return f'{mins:0>2}:{secs:0>2}'


async def vk_search(query: str, count=100) -> dict[int: dict]:
    service = ServiceAsync(os.getenv('VK_USER_AGENT'), os.getenv('VK_TOKEN'))
    try:
        songs = await service.search_songs_by_text(query, count)

        result = {}
        counter = 0
        try:
            for song in songs:
                result[counter] = {'name': song.title,
                                   'author': song.artist,
                                   'album': None,
                                   'bitrate': None,
                                   'duration_text': convert_song_duration(song.duration),
                                   'duration': song.duration,
                                   'album_cover_url': None,
                                   'url': song.url
                                   }
                counter += 1
        except Exception:
            pass

        return result
    except Exception as e:
        print(e)
        return {}


async def mail_ru_search(query, count=400):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Secret-Key': '%E5%97%D1%D9%E1%D3%CE%A0%9B%DF%D1%AE%D4%9D%DA%D6%D2%D7%9D%A7%99',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://my.mail.ru/music/search/Five',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    params = {
        'xemail': '',
        'ajax_call': '1',
        'func_name': 'music.search',
        'mna': '',
        'mnb': '',
        'arg_query': query,
        'arg_extended': '1',
        'arg_search_params': f'{{"music":{{"limit":{count}}},"playlist":{{"limit":50}},"album":{{"limit":10}},"artist":{{"limit":10}}}}',
        # '{"music":{"limit":400},"playlist":{"limit":50},"album":{"limit":10},"artist":{"limit":10}}'
        'arg_offset': '0',
        'arg_limit': '200',
        '_': '1688932574418',
    }

    async def request_with_params_and_headers(url, params, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as resp:
                return await resp.text()

    resp = await request_with_params_and_headers('https://my.mail.ru/cgi-bin/my/ajax', params, headers)

    resp_data = json.loads(resp)
    result = {}
    counter = 500
    try:
        for md in resp_data[3]['MusicData']:
            result[counter] = {'name': md['Name_Text_HTML'],
                               'author': md['Author'],
                               'album': md['Album'],
                               'bitrate': md['BitRate'],
                               'duration_text': md['Duration'],
                               'duration': md['DurationInSeconds'],
                               'album_cover_url': md['AlbumCoverURL'],
                               'url': 'https:' + md['URL']
                               }
            counter += 1
    except Exception as e:
        print(e)

    return result


def search_song(query: str) -> dict[int: dict]:
    """
    Search string and return list of tuples.
     Return {0: {name, author, album, ...}}
    """
    async def all_searches(query):
        res_vk = await vk_search(query, count=200)
        res_mail = await mail_ru_search(query, count=200)
        return {**res_vk, **res_mail}

    res = asyncio.run(all_searches(query))
    return res
