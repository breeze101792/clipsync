import time
# import clipboard
from utility.debug import *

import threading
from cliphal.clipmanager import *
from network.client import *

class Core:
    def __init__(self):
        self.flag_run = False

        self.service_threading = None
    def start(self):
        self.service_threading = threading.Thread(target=self.service)
        # self.service_threading.daemon=True
        self.service_threading.start()

    def network_callback(self, content):
        dbg_print(content.__str__)
        pass

    def service(self):
        srv_client = Client()
        srv_client.start()
        self.flag_run = True

        clipmgr = ClipManager()
        clip_ins = clipmgr.getClipInstance()

        while self.flag_run:
            time.sleep(0.1)

            recent_value = ""
            while True:
                clip_buffer = clip_ins.getBuffer()
                if clip_buffer != recent_value:
                    recent_value = clip_buffer
                    print("Value changed: %s" % str(recent_value)[:20])
                    srv_client.send(clip_buffer)
                time.sleep(0.1)

        srv_client.quit()
    def quit(self):
        self.flag_run = False

        # clipboard.paste()
        # clipboard.copy(text_buf)
