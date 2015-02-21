from functools import partial
import json
import logging
import os
from pathlib import Path
import requests

logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    resp = requests.get('https://api.imgur.com/3/gallery/', headers=headers)
    data = json.loads(resp.content)
    return map(lambda item: item['link'], data['data'])


def download_link(directory, link):
    logging.info('Downloading %s', link)
    image = requests.get(link)
    download_path = directory / os.path.basename(link)
    with download_path.open('wb') as f:
        f.write(image.content)


def main(client_id):
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    links = get_links(client_id)
    map(partial(download_link, download_dir), links[:10])


if __name__ == '__main__':
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    main(client_id)
