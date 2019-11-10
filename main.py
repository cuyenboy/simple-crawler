#!/usr/bin/env python3.7
# coding: utf-8

import requests
import pprint
import pickle
from requests_toolbelt.utils import dump


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename) -> object:
    try:
        with open(filename, 'rb') as input:
            return pickle.load(input)
    except FileNotFoundError:
        return None


pp = pprint.PrettyPrinter(indent=4)

# setup your own proxies
proxies = {
    'http': 'http://1.1.1.1:31',
    'https': 'https://1.1.2.1:32',
    'ftp': 'ftp://1.1.3.1:33'
}

# setup some extra headers common values, like userAgent & referer
headersToSend = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Referer': 'https://www.google.fr',
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
response = session.get('http://google.fr', headers=headersToSend, cookies=cookies, timeout=timeouts)

# dump all request data to debug your frames
data = dump.dump_all(response)
print(data.decode(response.encoding))

# dump several data
print('final_url = {}'.format(response.url))
print('status_code = {}'.format(response.status_code))
print('encoding = {}'.format(response.encoding))
print('apparent_encoding = '.format(response.apparent_encoding))
print('sent_headers = ')
print(pp.pprint(vars(response.request.headers)))
print('received_headers = ')
print(pp.pprint(vars(response.headers)))
print('cookies = ')
print(pp.pprint(vars(response.cookies)))

# save final object cookieJar for later use
save_object(response.cookies, 'cookies.jar')
