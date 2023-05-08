import threading
import time
import socket
import traceback
from network.package import *
from network.socketbase import *
from utility.debug import *

class ClientService(SocketBase):
    def __init__(self, connection, address, broadcast):
        super().__init__()
        self.setConnection(connection)
        self.address = address
        self.regPackageHandler(broadcast)

    def start(self):
        self.startService()
    def send(self, package):
        self.sendPackage(package)

# class ClientService(SocketConnection):
#     def __init__(self, connection, address, broadcast):
#         super().__init__()
#         self.connection = connection
#         self.address = address
#         self.broadcast = broadcast
#         self.flag_run = False

#         self.connection.settimeout(self.timeout)
#     def start(self):
#         self._service()
#     def send(self, package):
#         if package is not None:
#             dbg_debug('[{}]: send "{}"'.format(self.address, package))
#             self.connection.sendall(package.toBytes())
#     def _service(self):
#         self.flag_run = True

#         prev_socket_buffer = ''
#         while self.flag_run:
#             try:
#                 pkg = self.recievePackage(self.connection)
#                 if pkg is not None:
#                     self.broadcast(pkg)
#                 else:
#                     time.sleep(self.interval)
#             except socket.timeout as e:
#                 continue
#             except (BrokenPipeError, ConnectionResetError) as e:
#                 dbg_info('[{}] connection lost'.format(self.address), e)
#             except Exception as e:
#                 dbg_error('[{}]'.format(self.address), e)

#                 traceback_output = traceback.format_exc()
#                 dbg_error('[{}]'.format(self.address), traceback_output)
#                 time.sleep(self.interval)

#         dbg_info('[{}]: Connection End.'.format(self.address))
#         self.connection.close()
#     def quit(self):
#         self.flag_run = False
#         # if self.connection is not None:
#         #     self.connection.close()
#         # Test server close
#         try:
#             self.connection.shutdown(socket.SHUT_RDWR)
#         except:
#             pass
#         try:
#             self.connection.close()
#         except:
#             pass
#         # self.service_thread.join()

class Server(SocketConfig):
    def __init__(self):
        super().__init__()

        self.flag_run = False
        self.socket = None
        self.service_threading = None
        self.client_service = []

    def _wait_connection(self):
        wait_cnt = 100
        while wait_cnt > 0:
            if self.socket is not None:
                return True
            wait_cnt -= 1
            time.sleep(0.1)
        return False

    def quit(self):
        for each_client in self.client_service:
            each_client.quit()

        if self.socket is not None:
            self.socket.close()
        self.flag_run = False
        # self.service_threading.join()
    def start(self):
        self._service()

    def broadcast(self, package):
        self._wait_connection()
        # dbg_info('broadcast:',len(self.client_service), ', ',package, )
        for each_client in self.client_service:

            try:
                each_client.send(package)
            except Exception as e:
                dbg_debug(e)

                traceback_output = traceback.format_exc()
                dbg_debug(traceback_output)
    def startClient(self, client_svc):
        self.client_service.append(client_svc)
        dbg_debug('Start:', self.client_service)
        client_svc.start()
        self.client_service.remove(client_svc)
        dbg_debug('After:', self.client_service)
        # client_ins = 
        # del self.client_svc[client_svc]
    def _service(self):
        self.flag_run = True

        dbg_info('Start Service on {}:{}'.format(self.server_ip, self.server_port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(self.timeout)
        self.modifyBufferSize(self.socket)
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:

        self.socket.bind((self.server_ip, self.server_port))
        self.socket.listen()

        while self.flag_run:
            try:
                # don't need to delay, due to socket timeout
                conn, addr = self.socket.accept()
                dbg_info('connection from : {}'.format(addr))
                client_svc = ClientService(connection = conn, address = addr, broadcast=self.broadcast)

                client_thread = threading.Thread(target=self.startClient, args=(client_svc,))
                client_thread.daemon=True
                client_thread.start()

                time.sleep(self.interval)
            except socket.timeout as e:
                continue
            except Exception as e:
                dbg_error(e)

                traceback_output = traceback.format_exc()
                dbg_error(traceback_output)
                time.sleep(self.interval)

        # close connectiong
        dbg_info('End of Service ')
        self.socket.close()
        self.socket = None

if __name__ == "__main__":
    DebugSetting.setDbgLevel('Debug')
    srv = Server()
    # srv.setServerInfo(server_ip='127.0.0.1', server_port='65432')
    # srv.setServerInfo(server_ip='127.0.0.1')
    srv.setServerInfo(server_ip='10.1.1.17')
    srv.start()
