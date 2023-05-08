from cliphal.clipbase import *
from datetime import datetime
import time

class TestClip(ClipBase):
    def __init__(self):
        self._clip_buffer = ''
        self._g_cnt = 1
        self._interval = 30
        self._current_buffer = ''
    def setBuffer(self, byte_buffer):
        return byte_buffer
    def _interval_send(self):
        self._current_buffer = 'getBuffer'
    def _large_data_send(self):
        # self._interval = 10
        self._current_buffer = '''
And when this happens, and when we allow freedom ring, when we let it ring from every village and every hamlet, from every state and every city, we will be able to speed up that day when all of God's children, Black men and white men, Jews and Gentiles, Protestants and Catholics, will be able to join hands and sing in the words of the old Negro spiritual: Free at last. Free at last. Thank God almighty, we are free at last.
        '''
    def getBuffer(self):
        if self._g_cnt > 100000000:
            self._g_cnt = 1
        elif self._g_cnt % self._interval == 0:
            # self._interval_send()
            self._large_data_send()
            self._current_buffer += datetime.now().__str__()

        time.sleep(0.1)
        self._g_cnt += 1
        return self._current_buffer


