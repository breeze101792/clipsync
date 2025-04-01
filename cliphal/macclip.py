from cliphal.clipbase import *
import traceback
import subprocess
import sys

class MacClip(ClipBase):
    def __init__(self):
        pass
    def setBuffer(self, byte_buffer):
        return self.write_to_clipboard(byte_buffer)
    def getBuffer(self):
        return self.read_from_clipboard()
    def write_to_clipboard(self, output):
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        # process.communicate(output.encode('utf-8'))
        process.communicate(output)

    def read_from_clipboard(self):
        # return subprocess.check_output(
        #     'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')
        return subprocess.check_output(
            'pbpaste', env={'LANG': 'en_US.UTF-8'})
    @staticmethod
    def isSupported():
        if sys.platform == 'darwin':
            return True
        else:
            return False

    @staticmethod
    def getModeString():
        return 'macclip'
