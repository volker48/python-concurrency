import json
import logging
import os
from urllib.request import Request, urlopen
import requests


logger = logging.getLogger(__name__)


def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    req = Request('https://api.imgur.com/3/gallery/', headers=headers, method='GET')
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return map(lambda item: item['link'], data['data'])


def download_link(directory, link):
    logger.info('Downloading %s', link)
    image = requests.get(link)
    download_path = directory / os.path.basename(link)
    with download_path.open('wb') as f:
        f.write(image.content)

