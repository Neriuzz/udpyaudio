#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
import sys
import os

BASE_URL = 'https://www.urbandictionary.com/define.php?term='


def change_to_dir(search_term):
    PATH = f'udpyaudio/{search_term}'
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    os.chdir(PATH)


def get_sound_urls(content):
    SOUP = bs4(content, features='html.parser')
    try:
        return SOUP.findAll(
            'a', {'class': 'play-sound'})[1]['data-urls'].strip('[]').split(',')
    except:
        print('[!] Word does not have any downloadable audio pronunciations')
        sys.exit(1)


def get_content(url):
    try:
        return urlopen(url).read()
    except:
        print('[!] Word cannot be found in the Urban Dictionary')
        sys.exit(1)


def download_audio(url, search_term):
    sound_urls = get_sound_urls(get_content(url))
    change_to_dir(search_term)

    print('[!] Starting download...')
    for i, url in enumerate(sound_urls):
        mp3file = urlopen(url.strip('"'))
        with open('{}{}.mp3'.format(search_term, i), 'wb') as output:
            print('[+] Downloading {}/{}'.format(i + 1, len(sound_urls)))
            output.write(mp3file.read())


if __name__ == '__main__':
    os.chdir(os.path.expanduser('~/Documents'))
    search_term = ' '.join(sys.argv[1:])
    if search_term:
        url = (BASE_URL + search_term).replace(' ', '%20')
        download_audio(url, search_term)
        print('[!] Finished downloading audio files!')
        sys.exit(0)
    else:
        print('[!] Please provide a search term')
        sys.exit(1)
