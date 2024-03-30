import requests


def search_song(query: str) -> dict[int: dict]:
    """
    Search string and return list of tuples.
     Return {0: {name, author, album, ...}}
     """
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
        'arg_search_params': '{"music":{"limit":300},"playlist":{"limit":50},"album":{"limit":10},"artist":{"limit":10}}',
        'arg_offset': '0',
        'arg_limit': '200',
        '_': '1688932574418',
    }

    response = requests.get('https://my.mail.ru/cgi-bin/my/ajax', params=params, headers=headers)

    result = {}
    counter = 0
    try:
        for md in response.json()[3]['MusicData']:
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
    except Exception:
        pass

    return result


def download_song(song_id: str):
    pass
