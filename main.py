#!/usr/bin/env python3.7
# coding: utf-8

import requests
import pprint
import pickle
from requests_toolbelt.utils import dump
from requests import ConnectionError, Timeout, TooManyRedirects, RequestException
import cchardet as chardet


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename) -> object or None:
    try:
        with open(filename, 'rb') as input:
            return pickle.load(input)
    except FileNotFoundError:
        return None


pp = pprint.PrettyPrinter(indent=4)

# setup your own proxies

# SOCKS5 proxy for HTTP/HTTPS
# proxies = {
#     'http': "socks5://218.92.206.108:7302",
#     'https': "socks5://218.92.206.108:7302",
# }

# SOCKS4 proxy for HTTP/HTTPS
# proxies = {
#     'http': "socks4://221.214.212.149:45087",
#     'https': "socks4://221.214.212.149:45087",
# }

# HTTP proxy for HTTP/HTTPS
proxies = {
    # 'http': "http://13.66.25.52:80",
    # 'https': "https://207.191.15.166:38528",
}

# setup some extra headers common values, like userAgent & referer
headersToSend = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Referer': 'https://www.google.fr/',
}

# initialize session, and setup a max redirect to avoid bot traps
session = requests.Session()
session.max_redirects = 5

# load the saved cookieJar object... or not
# cookies = cookieJar object if file exists, None otherwise
cookies = load_object('cookies.jar')

# a very important thing : setup the timeout to scrape massively and not waste too much time
conn_timeout = 2
read_timeout = 5
timeouts = (conn_timeout, read_timeout)
try:
    response = session.get('https://www.google.fr/search?q=test', headers=headersToSend, cookies=cookies, timeout=timeouts, proxies=proxies)

    # use the power of cchardet to detect response content bytes encoding
    chardet_encoding = chardet.detect(response.content)

    # dump all request data to debug your frames
    data = dump.dump_all(response)
    print(data.decode(chardet_encoding['encoding']))

    print('------------------------------------------------------------')

    # dump several data
    print('final_url = {}'.format(response.url))
    print('status_code = {}'.format(response.status_code))
    print('encoding = {}'.format(response.encoding))
    print('apparent_encoding = {}'.format(response.apparent_encoding))
    print('chardet_encoding = {}'.format(chardet_encoding))
    print('sent_headers = {}'.format(response.request.headers))
    print('received_headers = {}'.format(response.headers))
    print('sent_body = {}'.format(response.request.body[:200] if response.request.body is not None else None))
    print('received_body = {}'.format(response.content.decode(chardet_encoding['encoding'])[:200] if response.content is not None else None))
    print('final_cookies = {}'.format(response.cookies))
    print('ok = {}'.format(response.ok))

    # save final object cookieJar for later use
    save_object(response.cookies, 'cookies.jar')

except ConnectionError as e:
    print('connectionError -> {}'.format(str(e)))
except Timeout as e:
    print('Timeout -> {}'.format(str(e)))
except TooManyRedirects as e:
    print('TooManyRedirects -> {}'.format(str(e)))
except RequestException as e:
    print('RequestException -> {}'.format(str(e)))
except BaseException as e:
    print('Exception -> {}'.format(str(e)))
