####
# This sample is published as part of the blog article at www.toptal.com/blog
# Visit www.toptal.com/blog and subscribe to our newsletter to read great posts
####
import logging
from pathlib import Path
from time import time
from functools import partial

from concurrent.futures import ProcessPoolExecutor

from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def create_thumbnail(size, path):
    """
    Creates a thumbnail of an image with the same name as image but with _thumbnail appended before the
    suffix.

    >>> create_thumbnail((128, 128), 'image.jpg')

    A new thumbnail image is created with the name image_thumbnail.jpg

    :param size: A tuple of the width and height of the image
    :param path: The path to the image file
    :return: None
    """
    path = Path(path)
    name = path.stem + '_thumbnail' + path.suffix
    thumbnail_path = path.with_name(name)
    image = Image.open(path)
    image.thumbnail(size)
    image.save(thumbnail_path)


def main():
    ts = time()
    # Partially apply the create_thumbnail method setting the size to 128x128 and returning a function of a single
    # argument
    thumbnail_128 = partial(create_thumbnail, (128, 128))

    # Create the executor in a with block so shut down is called when the block is exited
    with ProcessPoolExecutor() as executor:
        executor.map(thumbnail_128, Path('images').iterdir())
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()
