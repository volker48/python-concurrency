import logging
import os
from pathlib import Path

from imgur.gallery import get_links, download_link


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)


def main(client_id):
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    links = [l for l in get_links(client_id) if l.endswith(('.gif', '.jpg'))]
    for link in links[:10]:
        download_link(download_dir, link)


if __name__ == '__main__':
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    main(client_id)
