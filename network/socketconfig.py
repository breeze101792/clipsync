import socket
class SocketConfig:
    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 11320
        self.interval = 0.1
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
