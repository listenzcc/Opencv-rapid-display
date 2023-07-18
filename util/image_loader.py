"""
File: image_loader.py
Author: Chuncheng Zhang
Date: 2023-07-10
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-07-10 ------------------------
# Requirements and constants
import io
import cv2
import time
import hashlib
import requests
import threading
import traceback

import numpy as np

from .constant import *


# %% ---- 2023-07-10 ------------------------
# Function and class
class MyImage(object):
    """The base class for the image

    Load the image by the following methods:
    - from_local
    - from_url
    - from_PIL
    - from_bytes

    Use the self.image as the img information.
    """

    image_size = (800, 600)

    def __init__(self):
        self.image = None
        pass

    def get(self, key):
        """Get the key information from the img dictionary

        Args:
            key (str): The key to fetch

        Returns:
            ob: The value of the key in self.image
        """

        if not key in self.image:
            LOGGER.error('Failed to get key {}'.format(key))

        return self.image.get(key, None)

    def compute_img_everything(self, img: Image, img_id: str, require_detail_flag=False):
        """Compute all the information from the img object

        Args:
            img (Image): The input img object.
            image_id (str): The id of the image.
            require_detail_flag (Bool): Whether compute the detail of the image, default is False.

        Returns:
            dict: The information of the img object.
        """
        # Necessary checks
        if img is None:
            return None

        assert isinstance(
            img, Image.Image), 'The [img] must be an Image instance'

        # Constant
        format = 'jpeg'
        ext = 'jpg'
        mode = 'RGB'
        create_time = time.time()

        # Convert into RGB format
        if img.mode != mode:
            img = img.convert(mode=mode)

        if not all((img.size[0] == self.image_size[0], img.size[1] == self.image_size[1])):
            img = img.resize(self.image_size)

        bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        self.image = dict(
            img=img,
            bgr=bgr,
            img_id=img_id,
            # ---------------------------------
            ext=ext,
            mode=mode,
            format=format,
            create_time=create_time,
            # ---------------------------------
            bytes_io=None,
            md5_hash=None,
            get_bytes=None,
            get_hexdigest=None,
            # ---------------------------------
            unique_id=None,
            unique_fname=None,
        )

        # Compute the details in the separate thread
        if require_detail_flag:
            threading.Thread(target=self._compute_detail, daemon=True).run()

        return self.image

    def _compute_detail(self):
        """Compute the detail of the image,
        it is designed to be running in a separate thread.
        """
        tic = time.time()
        img = self.image['img']
        ext = self.image['ext']
        format = self.image['format']

        # Write into the BytesIO
        bytes_io = io.BytesIO()
        img.save(bytes_io, format=format)

        # Compute the md5 hash
        md5_hash = hashlib.md5()
        md5_hash.update(bytes_io.getvalue())

        self.image['bytes_io'] = bytes_io
        self.image['md5_hash'] = md5_hash
        self.image['get_bytes'] = bytes_io.getvalue
        self.image['get_hexdigest'] = md5_hash.hexdigest
        self.image['unique_id'] = md5_hash.hexdigest()
        self.image['unique_fname'] = '{}.{}'.format(md5_hash.hexdigest(), ext)

        toc = time.time()
        LOGGER.debug('Finish detail ({:0.4f}) for image {}'.format(
            toc - tic,
            self.image['unique_id']))

        return

    def null(self):
        return

    def from_local(self, path: Path, img_id: str):
        """Init the image from a local image path,
        all the file paths that can be converted into Path objects are allowed.

        Args:
            path (Path): The local image path.
            image_id (str): The id of the image.

        Returns:
            self (MyImage);
            thread (Thread): The current thread of processing the image,
                             wait it until finishes.
        """
        try:
            self.image = None
            img = Image.open(Path(path))

            thread = threading.Thread(
                target=self.compute_img_everything, args=(img, img_id), daemon=True)
            thread.start()
        except:
            thread = threading.Thread(target=self.null, daemon=True)
            thread.start()
            LOGGER.error('Can not read image from local path: {}'.format(path))
            traceback.print_exc()
        return self, thread

    def from_url(self, url: str, img_id: str):
        """Init the image from a url

        Args:
            url (str): The remote url of the image.
            image_id (str): The id of the image.

        Returns:
            dict: The img info of the image
        """
        try:
            self.image = None
            img = Image.open(requests.get(url, stream=True).raw)
            self.compute_img_everything(img, img_id)
            # print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from url: {}'.format(url))
            traceback.print_exc()
        return self

    def from_PIL(self, img: Image, img_id: str):
        """Init the image from a Image object

        Args:
            img (Image): The Image object.
            image_id (str): The id of the image.

        Returns:
            dict: The img info of the image
        """
        try:
            self.image = None
            self.compute_img_everything(img, img_id)
            # print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from img')
            traceback.print_exc()
        return self

    def from_bytes(self, raw: bytes, img_id: str):
        """Init the image from the raw bytes

        Args:
            raw (bytes): The bytes of the image.
            image_id (str): The id of the image.

        Returns:
            dict: The img info of the image
        """

        try:
            self.image = None
            img = Image.open(raw)
            self.compute_img_everything(img, img_id)
            # print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from bytes')
            traceback.print_exc()
        return self


def read_local_images(folder, limit=200):
    """Read the local images in the given folder with the number limit.

    It supports all the files in the folder are image files.

    It uses the read_from_file_list() to read the files.

    Args:
        folder (Path or str): The folder to read the images from;
        limit (int, optional): The limit of reading images. Defaults to 20.

    Returns:
        file_list (list): The file_list;
        images (list): The images in the object of MyImage;
        tag_table (dict): The tag table of the img_id.

    """
    folder = Path(folder)
    if not folder.is_dir():
        LOGGER.error('Folder does not exist: {}'.format(folder))
        return

    # (path, img_id, tag)
    file_list = [(path, 'nothing.' + path.name, 'nothing')
                 for path in tqdm(folder.iterdir(), 'Find files')
                 if path.is_file()][:limit]

    images, tag_table = read_from_file_list(file_list)
    return file_list, images, tag_table

    raws = [MyImage().from_local(f, f.name)
            for f in tqdm(files, 'Load images')]

    images = [e for e in raws if e.image is not None]

    LOGGER.info('Loaded ({} | {}) images from {}'.format(
        len(images), len(files), folder))

    return images


def read_from_file_list(file_list):
    """Read images from the file_list.

    The elements are the tuple of (path, img_id, tag) 

    Args:
        file_list (list): The file_list to be read;
        path (Path): The path of the image;
        img_id (str): The img_id of the image;
        tag (str): The tag of the image;

    Returns:
        _type_: _description_
    """
    images = []
    threads = []
    tag_table = dict()

    for path, img_id, tag in tqdm(file_list, 'Reading files...'):
        path = Path(path)

        my_img, thread = MyImage().from_local(path, img_id)
        threads.append(thread)
        images.append(my_img)

        if img_id in tag_table:
            LOGGER.warning('Repeat img_id, {} = {}'.format(
                img_id, tag_table[img_id]))

        tag_table[img_id] = tag

    for t in tqdm(threads, 'Join threads...'):
        t.join()

    LOGGER.debug('Loading images finished.')

    for my_img in images:
        if my_img.image is not None:
            pass
        else:
            LOGGER.error(
                'Can not load image {}, {}, {}'.format(tag, img_id, path))

    images = [e for e in images if e.image is not None]

    LOGGER.debug('Loaded {} | {} images from file_list, tags are {}'.format(
        len(images), len(file_list), set([e for e in tag_table.values()])))

    return images, tag_table


# %%


# %% ---- 2023-07-10 ------------------------
# Play ground
if __name__ == '__main__':
    read_local_images(Path(os.environ['OneDriveConsumer'],
                           'Pictures', 'DesktopPictures'))


# %% ---- 2023-07-10 ------------------------
# Pending


# %% ---- 2023-07-10 ------------------------
# Pending
