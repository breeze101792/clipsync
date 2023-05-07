import threading
import time
import socket
import traceback
from network.package import *
from network.socketbase import *
from utility.debug import *

class Client(SocketBase):
    def __init__(self):
        super().__init__()
    def start(self):
        self.startThread()
    def send(self, content):
        self.sendData(content)


# class Client(SocketConnection):
#     def __init__(self):
#         super().__init__()
#         self.flag_run = False

#         self.socket = None
#         self.service_threading = None
#         self._package_handler = self._def_pkg_hadler
#     def _def_pkg_hadler(self, content):
#         dbg_print('Content:', content.__str__())

#     def regPackageHandler(self, handler):
#         self._package_handler = handler
#     def _wait_connection(self):
#         wait_cnt = 100
#         while wait_cnt > 0:
#             if self.socket is not None:
#                 return True
#             wait_cnt -= 1
#             time.sleep(self.interval)
#         return False

#     def send(self, content):
#         self._wait_connection()
#         try:
#             tmp_pkg = Package()
#             tmp_pkg.content = content
#             self.socket.sendall(tmp_pkg.toBytes())
#         except Exception as e:
#             print(e)
#             traceback_output = traceback.format_exc()
#             print(traceback_output)
#         # finally:
#         #     pass
#     def start(self):
#         self.service_threading = threading.Thread(target=self._service)
#         self.service_threading.daemon=True
#         self.service_threading.start()

#     def _service(self):
#         self.flag_run = True

#         dbg_info('Connect to remote Service on {}:{}'.format(self.server_ip, self.server_port))
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.connect((self.server_ip, self.server_port))
#         self.modifyBufferSize(self.socket)
#         # self.socket.sendall(b"Hello, world")
#         prev_socket_buffer = ''
#         while self.flag_run:
#             try:
#                 pkg = self.recievePackage(self.socket)
#                 if pkg is not None:
#                     self._package_handler(pkg.content)
#                 else:
#                     time.sleep(self.interval)

#             except Exception as e:
#                 dbg_error(e)

#                 traceback_output = traceback.format_exc()
#                 dbg_error(traceback_output)
#             finally:
#                 time.sleep(self.interval)

#         # close connectiong
#         dbg_info('End of Service ')
#         self.socket.close()
#         self.socket = None
#     def quit(self):
#         self.flag_run = False
#         if self.socket is not None:
#             self.socket.close()

#         self.service_threading.join()

if __name__ == "__main__":

    DebugSetting.setDbgLevel('Debug')
    client = Client()
    client.setServerInfo(server_ip='10.1.1.17')
    client.start()
    client.send('Hello Word')
    time.sleep(3)
