import time
# import clipboard
from utility.debug import *

import threading
from cliphal.clipmanager import *
from network.client import *

class Core:
    def __init__(self):
        self.flag_run = False
        self.previous_clips = ''

        clipmgr = ClipManager()
        self.clip_ins = clipmgr.getClipInstance()

        self.service_threading = None
        self.server_ip = '127.0.0.1'
        self.server_port = 65432

    def setServerInfo(self, server_ip = '127.0.0.1', server_port=65432):
        self.server_ip = server_ip
        self.server_port = server_port

    def start(self):
        self.service_threading = threading.Thread(target=self.service)
        # self.service_threading.daemon=True
        self.service_threading.start()

    def network_callback(self, content):
        dbg_print(content.__str__)
        self.previous_clips = content
        self.clip_ins.setBuffer(content)

    def service(self):
        srv_client = Client()
        srv_client.setServerInfo(server_ip=self.server_ip, server_port=self.server_port)
        srv_client.start()
        self.flag_run = True

        while self.flag_run:
            time.sleep(0.1)

            while True:
                clip_buffer = self.clip_ins.getBuffer()
                if clip_buffer != self.previous_clips:
                    self.previous_clips = clip_buffer
                    print("Value changed: %s" % str(self.previous_clips)[:20])
                    srv_client.send(clip_buffer)
                time.sleep(0.1)

        srv_client.quit()
    def quit(self):
        self.flag_run = False

        # clipboard.paste()
        # clipboard.copy(text_buf)
