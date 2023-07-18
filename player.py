"""
File: player.py
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

from util.constant import *
from util.toolbox import PreciseClock, pop, linear_interpolate, get_monitor_size
from util.image_loader import read_local_images


# %% ---- 2023-07-10 ------------------------
# Function and class
class DynamicOptions(object):
    """
    Dynamic Options during the runtime.
    """

    def __init__(self):
        self.winname = CONFIG.project.name
        pass

    def start(self):
        """Start the options

        - Set the rsvp_loop_flag,
        - Init the recording with the empty list.
        """
        self.rsvp_loop_flag = True
        self.recording = []

    def record(self, dct):
        """Record the dct in a separate threading.

        Args:
            dct (dict): The dict to be recorded.
        """
        threading.Thread(target=self.recording.append, args=(dct, )).start()

    def stop(self):
        """Stop the options
        """
        self.rsvp_loop_flag = False

    def save_recording(self, path='time_recording.csv'):
        path = Path(path)

        if path.is_file():
            LOGGER.warning('Saving recording to existing file {}'.format(path))

        table = pd.DataFrame(DY_OPT.recording)
        table.to_csv(path)

        LOGGER.debug('Saved recording to {}'.format(path))
        return table


DY_OPT = DynamicOptions()


def cv2_poll_key(t):
    """Record the key-press during the latest poll,
    it also refreshes the cv2.imshow.
    So, call it after every cv2.imshow.

    For now, it only records the first key-press during the range.

    Args:
        t (float): The timestamp in float.

    Returns:
        int: The key code for the press, -1 refers no key pressed.
    """
    code = cv2.pollKey()

    if code == -1:
        return code

    print('Key pressed {}, {}'.format(code, t))

    if code == ord('q'):
        DY_OPT.stop()

    while cv2.pollKey() > -1:
        continue

    DY_OPT.record(dict(
        time=t,
        code=code,
        recordType='KeyPress'
    ))
    return code


def uint8(x):
    """Convert ndarray x to uint8 format

    Args:
        x (numpy.Array): ndarray.

    Returns:
        numpy.Array: The ndarray in uint8 format.
    """
    return x.astype(np.uint8)


class VeryFastVeryStableBuffer(object):
    def __init__(self, images, m=5):
        self.images = images
        self.m = m
        self.buffer = []
        self.size = 0

    def clear_buffer(self):
        [self.pop() for _ in range(self.size)]
        self.size = 0
        return

    def pop(self):
        mats = [self.buffer.pop(0) for _ in range(self.m)]
        self.size -= 1

        threading.Thread(target=self.auto_append, daemon=True).start()

        return mats

    def auto_append(self):
        image = pop(self.images)
        mat1 = image.get('bgr')
        id = image.get('image_id')
        mat2 = pop(self.images, shift_flag=False).get('bgr')

        for e in linear_interpolate(mat1, mat2, self.m):
            self.buffer.append((id, uint8(e)))
            # Only attach the id to the first element
            id = None

        self.size += 1

        return self.size

    def loop(self):
        threading.Thread(target=self._loop, args=(), daemon=True).start()
        return

    def _loop(self, sleep_interval=20):
        secs = sleep_interval / 1000
        while True:
            if self.size < 10:
                self.auto_append()

            time.sleep(secs)
            print('Loop', self.size, len(self.buffer))


class CV2FullScreen(object):
    def __init__(self, winname=DY_OPT.winname):
        self.winname = winname
        self.setup_full_screen()
        pass

    def setup_full_screen(self):
        """Setup the cv2 for full screen display
        """
        # Set the cv2 window to full-screen-display.
        # Set the window to full-screen.
        cv2.namedWindow(self.winname, cv2.WND_PROP_FULLSCREEN)
        # Set the window property to fit the full-screen, disable the top bar and something like that.
        cv2.setWindowProperty(self.winname,
                              cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # The window_position is (x, y, width, height)
        image_rect = cv2.getWindowImageRect(DY_OPT.winname)
        self.image_rect = image_rect

        self.generate_background()

        LOGGER.debug('Setup cv2 window {} with full screen, the image rect is {}'.format(
            self.winname, self.image_rect))

        return

    def generate_background(self, image_rect=None, r=100, g=100, b=100):
        """Generate the background for the display.

        Args:
            image_rect (4 elements tuple, optional): The rect for the image in the format of (x, y, width, height). Defaults to None, refers using self.image_rect.
            r (int, optional): R channel. Defaults to 100.
            g (int, optional): G channel. Defaults to 100.
            b (int, optional): B channel. Defaults to 100.

        Returns:
            3d array: The BGR background image in the format of (height, width, 3)
        """
        if image_rect is None:
            image_rect = self.image_rect

        background = np.zeros((image_rect[3], image_rect[2], 3))
        background[:, :, 0] = b
        background[:, :, 1] = g
        background[:, :, 2] = r
        background = uint8(background)

        LOGGER.debug(
            'Generated background image ({})'.format(background.shape))

        self.background = background

        return background

    def place_in_center(self, bgr, background=None):
        """Place the bgr into the center of the background image.

        Args:
            bgr (3d array): The image in BGR format, the size is (height, width, 3).
            background (3d array, optional): The larger background as the same format as the bgr. Defaults to None, refers using self.background.

        Returns:
            3d array: The new background with the bgr in the center of it.
        """

        if background is None:
            background = self.background

        bg_height, bg_width = background.shape[:2]
        img_height, img_width = bgr.shape[:2]

        x_offset = (bg_width - img_width) // 2
        y_offset = (bg_height - img_height) // 2

        background[y_offset:y_offset+img_height,
                   x_offset:x_offset+img_width] = bgr

        return background


# %% ---- 2023-07-10 ------------------------
# Play ground
images = read_local_images(Path(os.environ['OneDriveConsumer'],
                                'Pictures', 'DesktopPictures'))

width, height = get_monitor_size()

# %%

# %% ---- 2023-07-10 ------------------------
# Pending
interval = 100  # milliseconds
display_seconds = 60  # seconds
frames = int(display_seconds / (interval / 1000))
print('Display with {} frames'.format(frames))

vfvsb = VeryFastVeryStableBuffer(images, m=1)
pc = PreciseClock(interval)
cv2_full_screen = CV2FullScreen(DY_OPT.winname)


# Pre install the vfvsb with 5 image pairs.
for _ in range(5):
    vfvsb.auto_append()

# Fetch one image pair from the vfvsb.
pairs = vfvsb.pop()

for _ in range(vfvsb.m):
    id, bgr = pairs.pop(0)
    cv2.imshow(DY_OPT.winname, cv2_full_screen.place_in_center(bgr))
    cv2.waitKey(100)

print('Press any key to continue')
cv2.waitKey()
print('Start...')

DY_OPT.start()

frame_idx = 0
time_recording = []

pc.start()
while (frame_idx < frames) and DY_OPT.rsvp_loop_flag:
    if pc.count() < frame_idx:
        continue

    pairs = vfvsb.pop()
    id, bgr = pairs.pop(0)

    if frame_idx % 2 == 1:
        bgr[:100, :100] = 255
    else:
        bgr[:100, :100] = 0

    t = time.time()
    cv2.imshow(DY_OPT.winname, cv2_full_screen.place_in_center(bgr))

    cv2_poll_key(t)

    time_recording.append((frame_idx, id, t))
    DY_OPT.record(dict(
        time=t,
        imgId=id,
        frameIdx=frame_idx,
        recordType='displayImage'
    ))
    print('Display {: 4d} at {:.4f} for {}'.format(
        frame_idx, time_recording[-1][-1], id))

    frame_idx += 1


cv2.waitKey(1)
DY_OPT.stop()

print(DY_OPT.save_recording('time_recording.csv'))


# %% ---- 2023-07-10 ------------------------
# Pending
# Call the check_time_recording function.
os.system('python check_time_recording.py')

# %%


# %%
