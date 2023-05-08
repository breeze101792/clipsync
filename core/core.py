import time
# import clipboard
from utility.debug import *

import threading
from cliphal.clipmanager import *
from network.client import *
from network.crypto import *

class Core:
    def __init__(self):
        self.flag_run = False
        self.previous_clips = ''

        clipmgr = ClipManager()
        self.clip_ins = clipmgr.getClipInstance()
        self.previous_clips = self.clip_ins.getBuffer()

        # self.service_threading = None
        self.server_ip = None
        self.server_port = None

        # cryption
        self.crypto = Crypto()
        self.crypto.keyGen('clipsync')

    def setServerInfo(self, server_ip = None, server_port=None):
        self.server_ip = server_ip
        self.server_port = server_port

    def start(self):
        # self.service_threading = threading.Thread(target=self._service)
        # self.service_threading.daemon=True
        # self.service_threading.start()
        self._service()

    def network_callback(self, package):
        # dbg_print(content.__str__())
        if package.content is not None and len(package.content) > 0:
            self.previous_clips = package.content
            decrypted_content = self.crypto.decrypt(package.content).decode(encoding="utf8")
            self.clip_ins.setBuffer(decrypted_content)
            dbg_info('Set clipboard {}: "{}"'.format(len(decrypted_content) ,decrypted_content))
        else:
            dbg_debug('buffer invalid: {}: "{}"'.format(len(package.content) ,package.content))

    def _service(self):
        srv_client = Client()
        srv_client.setServerInfo(server_ip=self.server_ip, server_port=self.server_port)
        srv_client.regPackageHandler(self.network_callback)
        srv_client.createConnection()
        srv_client.start()
        self.flag_run = True

        while self.flag_run:
            try:
                clip_buffer = self.clip_ins.getBuffer()
                if len(clip_buffer) > 0 and clip_buffer != self.previous_clips:
                    self.previous_clips = clip_buffer
                    # dbg_print("Value changed: %s" % str(self.previous_clips)[:20])
                    dbg_info("clipboard changed, notify server. buffer: {}\n".format(clip_buffer))
                    # srv_client.send(clip_buffer)
                    dbg_print(clip_buffer)
                    srv_client.send(self.crypto.encrypt(clip_buffer.encode('utf8')))
            except Exception as e:
                dbg_error(e)

                traceback_output = traceback.format_exc()
                dbg_error(traceback_output)
            finally:
                time.sleep(0.1)

        self.flag_run = False
        srv_client.quit()
    def quit(self):
        self.flag_run = False

        # clipboard.paste()
        # clipboard.copy(text_buf)
