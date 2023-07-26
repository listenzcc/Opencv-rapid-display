# %%
import time
import threading

from . import setPortAddress, setData

# %%

# %%


class Parallel(object):
    def __init__(self):
        self.address = None
        self.buffer = []
        pass

    def reset(self, address):
        self.address = address
        address_hex = int(address, 16)
        setPortAddress(address_hex)
        setData(0)
        self.run_forever()

    def sending_loop(self):
        while True:
            self._send(verbose=True)
            time.sleep(0.001)

    def run_forever(self):
        t = threading.Thread(target=self.sending_loop, daemon=True)
        t.start()

    def send(self, value, verbose=True):
        self.buffer.append(value)

        # t = threading.Thread(target=self._send, args=(verbose,), daemon=True)
        # t.start()

        return time.time()

    def _send(self, verbose):
        n = len(self.buffer)
        buffer = set([self.buffer.pop(0) for _ in range(n)])

        value = sum(buffer)

        if value == 0:
            return

        if self.address is None:
            print('Send failed since the Parallel is not set')
        else:
            setData(value)
            time.sleep(0.001)
            setData(0)

        if verbose:
            print('Sent: {} to {}'.format(value, self.address))
