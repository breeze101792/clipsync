import time
import clipboard
from utility.debug import *
class Core:
    def __init__(self):
        pass
    def start(self):
        while True:
            time.sleep(0.1)

            dbg_info("")
            recent_value = ""
            while True:
                tmp_value = clipboard.paste()
                if tmp_value != recent_value:
                    recent_value = tmp_value
                    print("Value changed: %s" % str(recent_value)[:20])
                time.sleep(0.1)
    def quit(self):
        pass

        # clipboard.paste()
        # clipboard.copy(text_buf)
