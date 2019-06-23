#!/usr/bin/evn python3

from bs4 import BeautifulSoup as bs4
import urllib2, os, sys

BASE_URL = 'https://www.urbandictionary.com/define.php?term='

def download_audio(url, search_term):

    try:
        content = urllib2.urlopen(url).read()
    except:
        print('No such term exists in the Urban Dictionary!')
        sys.exit(1)

    soup = bs4(content, 'lxml')

    try:
        sound_urls = soup.findAll('a', {'class': 'play-sound'})[1]['data-urls'].strip('[]').split(',')
    except:
        print('No audio pronunciation found for this search term')
        sys.exit(1)

    path = r'udpyaudio/{}'.format(search_term)


    if not os.path.exists(path):
        os.makedirs(path)
    
    os.chdir(path)

    i = 0
    for url in sound_urls:
        mp3file = urllib2.urlopen(url.strip('"'))
        with open('{}{}.mp3'.format(search_term, i), 'wb') as output:
            print('Saving file {}/{}'.format(i + 1, len(sound_urls)))
            output.write(mp3file.read())
        i += 1


if __name__ == '__main__':
    os.chdir(os.path.expanduser('~/Documents'))
    search_term = ' '.join(sys.argv[1:])

    if search_term:
        url = (BASE_URL + search_term).replace(' ', '%20')
        download_audio(url, search_term)
        print('Finished downloading audio files!')
        sys.exit(0)
    else:
        print('Please provide a search term')
        sys.exit(1)
