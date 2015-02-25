import json
import logging
import os
from pathlib import Path
from queue import Queue
from threading import Thread
from time import time
from urllib.request import Request, urlopen


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def download_link(self, directory, link):
        download_path = directory / os.path.basename(link)
        with urlopen(link) as image, download_path.open('wb') as f:
            f.write(image.readall())

    def run(self):
        while True:
            directory, link = self.queue.get()
            self.download_link(directory, link)
            self.queue.task_done()


def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    req = Request('https://api.imgur.com/3/gallery/', headers=headers, method='GET')
    with urlopen(req) as resp:
        data = json.loads(resp.readall().decode('utf-8'))
    return map(lambda item: item['link'], data['data'])


def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = [l for l in get_links(client_id) if l.endswith(('.gif', '.jpg'))]
    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    for link in links[:20]:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    queue.join()
    print('Took {}'.format(time() - ts))

if __name__ == '__main__':
    main()
