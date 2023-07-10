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
import time
import hashlib
import requests
import threading
import traceback

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

    def compute_img_everything(self, img: Image, image_id: str, require_detail_flag=False):
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
        img = img.resize(self.image_size)

        self.image = dict(
            img=img,
            image_id=image_id,
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

    def from_local(self, path: Path, image_id: str):
        """Init the image from a local image path,
        all the file paths that can be converted into Path objects are allowed.

        Args:
            path (Path): The local image path.
            image_id (str): The id of the image.

        Returns:
            dict: The img info of the image
        """
        try:
            self.image = None
            img = Image.open(Path(path))
            self.compute_img_everything(img, image_id)
            print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from local path: {}'.format(path))
            traceback.print_exc()
        return self

    def from_url(self, url: str, image_id: str):
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
            self.compute_img_everything(img, image_id)
            print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from url: {}'.format(url))
            traceback.print_exc()
        return self

    def from_PIL(self, img: Image, image_id: str):
        """Init the image from a Image object

        Args:
            img (Image): The Image object.
            image_id (str): The id of the image.

        Returns:
            dict: The img info of the image
        """
        try:
            self.image = None
            self.compute_img_everything(img, image_id)
            print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from img')
            traceback.print_exc()
        return self

    def from_bytes(self, raw: bytes, image_id: str):
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
            self.compute_img_everything(img, image_id)
            print('Created image: {}'.format(self.image))
        except:
            LOGGER.error('Can not read image from bytes')
            traceback.print_exc()
        return self


def load_folder(folder, limit=20):
    folder = Path(folder)
    if not folder.is_dir():
        LOGGER.error('Folder does not exist: {}'.format(folder))
        return

    files = [f for f in tqdm(folder.iterdir(), 'Find files')
             if f.is_file()][:limit]

    raws = [MyImage().from_local(f, f.name)
            for f in tqdm(files, 'Load images')]

    images = [e for e in raws if e.image is not None]

    LOGGER.info('Loaded ({} | {}) images from {}'.format(
        len(images), len(files), folder))

    return images

# %%


# %% ---- 2023-07-10 ------------------------
# Play ground
if __name__ == '__main__':
    load_folder(Path(os.environ['OneDriveConsumer'],
                'Pictures', 'DesktopPictures'))


# %% ---- 2023-07-10 ------------------------
# Pending


# %% ---- 2023-07-10 ------------------------
# Pending
