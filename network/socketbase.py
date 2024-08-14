import socket
from network.package import *

import threading
import time
import traceback

class SocketConfig:
    def __init__(self):
        self.server_ip = '0.0.0.0'
        self.server_port = 11320
        self.interval = 1
        self.timeout = 0.1
        self.buffer_size = 8192
        self.recv_buffer = self.buffer_size

    def setServerInfo(self, server_ip = None, server_port=None):
        if server_ip is not None:
            self.server_ip = server_ip
        if server_port is not None:
            self.server_port = server_port
    def modifyBufferSize(self, socket_connection):
        SEND_BUF_SIZE = self.buffer_size
        RECV_BUF_SIZE = self.buffer_size

        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # print "Buffer size [Before]: %d" %bufsize

        socket_connection.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        socket_connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
        socket_connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)

        # bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # print( "Buffer size [After]: %d" %bufsize)

class SocketBase(SocketConfig):
    def __init__(self):
        super().__init__()
        self.flag_run = False
        self.address = 'no impl'

        self.socket = None
        self.service_threading = None
        self._package_handler = self._def_pkg_hadler
    def _def_pkg_hadler(self, content):
        dbg_print('Content:', content.__str__())

    def regPackageHandler(self, handler):
        self._package_handler = handler

    def _wait_connection(self):
        wait_cnt = 100
        while wait_cnt > 0:
            if self.socket is not None:
                return True
            wait_cnt -= 1
            time.sleep(self.interval)
        return False
    def setConnection(self, connection):
        self.socket = connection
    def createConnection(self, retry=False):
        retry_sleep=10
        while True:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_ip, self.server_port))
                self.modifyBufferSize(self.socket)
                dbg_info('Connect to Server({}:{})'.format(self.server_ip, self.server_port))
                break
            except socket.timeout as e:
                dbg_error('Connect Timeout, Please fix networking. Sleep for {} seconds'.format(retry_sleep))
                dbg_error('[{}]'.format(self.address), e)

                traceback_output = traceback.format_exc()
                dbg_error('[{}]'.format(self.address), traceback_output)
                # prevending conection error
                time.sleep(retry_sleep)
                if retry is True:
                    continue
                else:
                    raise e

    def reConnection(self):
        if self.socket is not None:
            self.socket.close()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))
        self.modifyBufferSize(self.socket)
    def connectionLostHandler(self):
        # default empty, not all socket will need this function
        return False
    def sendPackage(self, package):
        self._wait_connection()
        if package is not None:

            # hard coded to 01
            package.type = '01'
            package.srcip = self.socket.getsockname()[0]
            package.destip = self.socket.getpeername()[0]

            dbg_debug('[{}]: send "{}"'.format(self.address, package))

            self.socket.sendall(package.toBytes())
    def sendData(self, content):
        tmp_pkg = Package()
        tmp_pkg.content = content
        self.sendPackage(tmp_pkg)

    def startThread(self):
        self.service_threading = threading.Thread(target=self.service)
        self.service_threading.daemon=True
        self.service_threading.start()
    def startService(self):
        self.service()

    def service(self):
        self.flag_run = True

        prev_socket_buffer = ''
        while self.flag_run:
            try:
                pkg = self.recievePackage(self.socket)
                if pkg is not None:
                    self._package_handler(pkg)
                 # else:
                 #     # no need to delay, since we have timeout on recieve
                 #     time.sleep(self.interval)
            except socket.timeout as e:
                continue
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
                dbg_info('[{}] socket lost'.format(self.address), e)
                if self.connectionLostHandler() is False:
                    return
                else:
                    dbg_info('[{}] socket reconnected.'.format(self.address), e)

            except Exception as e:
                dbg_error('[{}]'.format(self.address), e)

                traceback_output = traceback.format_exc()
                dbg_error('[{}]'.format(self.address), traceback_output)
                # prevending conection error
                time.sleep(self.interval)

        dbg_info('[{}]: Connection End.'.format(self.address))
        self.socket.close()

    def recievePackage(self, socket):
        data = socket.recv(Package.HEADER_SIZE)
        if len(data) != 0:
            dbg_debug('Data: "{}"'.format(data))

            pkg = Package()
            missing_len = pkg.fromBytes(data)
            if missing_len == 0:
                dbg_warning('Read first header size fail, clean socket buffer size')
                self.socket.recv(self.buffer_size)
            recv_cnt = 5
            while missing_len != 0 and recv_cnt > 0:
                missing_len = pkg.fromBytes(data)
                # we still have missing byte, delay for waiting transmission
                time.sleep(0.01)
                if missing_len > 0:
                    dbg_debug('Byte missing: ', missing_len, ', ', data[-64:])
                    missing_byte = socket.recv(missing_len)
                    data = data+missing_byte
                    pkg.fromBytes(data)

            # package_handler(pkg)
            return pkg
        else:
            return None
            # time.sleep(self.interval)
    def getPeerHostname(self):
        return  self.socket.getpeername()

    def quit(self):
        self.flag_run = False
        if self.socket is not None:
            self.socket.close()

        if self.service_threading is not None:
            self.service_threading.join()
            self.service_threading = None

