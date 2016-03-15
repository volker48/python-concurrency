####
# This sample is published as part of the blog article at www.toptal.com/blog
# Visit www.toptal.com/blog and subscribe to our newsletter to read great posts
####

import logging
import os
from time import time
import asyncio

import aiohttp
from download import setup_download_dir, get_links


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asyncio.coroutine
def async_download_link(directory, link):
    download_path = directory / os.path.basename(link)
    response = yield from aiohttp.request('get', link)
    with download_path.open('wb') as f:
        while True:
            chunk = yield from response.content.read(1000)
            if not chunk:
                break
            f.write(chunk)
    logger.info('Downloaded %s', link)


def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    loop = asyncio.get_event_loop()
    # Instead of asyncio.async you can also use loop.create_task, but loop.create_task is only available
    # in Python >= 3.4.2
    tasks = [asyncio.async(async_download_link(download_dir, l)) for l in get_links(client_id) if l.endswith('.jpg')]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    logger.info('Took %s seconds to complete', time() - ts)


if __name__ == '__main__':
    main()
