####
# This sample is published as part of the blog article at www.toptal.com/blog
# Visit www.toptal.com/blog and subscribe to our newsletter to read great posts
####

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time import time

from download import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)

    # By placing the executor inside a with block, the executors shutdown method will be called cleaning up threas
    # By default, the executor sets number of workers to 5 times the number of CPUs.
    with ThreadPoolExecutor() as executor:

        # Create a new partially applied function that stores the directory argument.
        # This allows the download_link function that normally takes two arguments to work
        # with the map function that expects a function of a single argument
        fn = partial(download_link, download_dir)

        # Executes fn concurrently using threads on the links iterable. The timeout is for the entire process not a single
        # call so downloading all images must complete within 30 seconds.
        executor.map(fn, links, timeout=30)
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()
