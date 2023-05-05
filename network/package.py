import time
import json
import traceback
from utility.debug import *
"""
type
src ip
dest ip
len
content
"""
class Package:
    def __init__(self):
        self.data_dict = {
            'type':'',
            'srcip':'',
            'destip':'',
            'length':'',
            'content':''
        }
        self._header_size = 64

    @staticmethod
    def fromBytes_json(byte_data):
        byte_buf = byte_data.decode(encoding="utf-8", errors="strict")
        tmp_json = json.loads(byte_buf)

        tmp_pkg = Package()
        tmp_pkg.type    = tmp_json['type']
        tmp_pkg.srcip   = tmp_json['srcip']
        tmp_pkg.destip  = tmp_json['destip']
        tmp_pkg.length  = tmp_json['length']
        tmp_pkg.content = tmp_json['content']
        dbg_debug(tmp_pkg)
        # dbg_debug(Package.__fromByte(byte_data))
        return tmp_pkg

    def toBytes_json(self):
        tmp_json = json.dumps(self.data_dict, indent=2)
        byte_buf = tmp_json.__str__().encode()
        # dbg_debug(self.__toByte())
        return byte_buf

    def fromBytes(self, byte_data):
        # dbg_debug('All Data: ', len(byte_data), byte_data)
        # dbg_debug('Header:   ', len(byte_data[:self._header_size]), byte_data[:self._header_size])
        # dbg_debug('Content:  ', len(byte_data[self._header_size:]), byte_data[self._header_size:])
        current_len = 0
        try:
            if len(byte_data) < self._header_size:
                dbg_debug('bytedata shorter than header size:  ', len(byte_data), ', ',self._header_size)
                return self._header_size - len(byte_data)
            header_buffer = byte_data[:self._header_size].decode('ascii')
            content_buffer = byte_data[self._header_size:].decode('utf8')

            # tmp_pkg = Package()
            self.data_dict['type']    = header_buffer[current_len:current_len+2].strip()
            current_len += 2
            self.data_dict['srcip']   = header_buffer[current_len:current_len+15].strip()
            current_len += 15
            self.data_dict['destip']  = header_buffer[current_len:current_len+15].strip()
            current_len += 15

            self.data_dict['length']  = int(header_buffer[current_len:current_len+8].strip())
            if len(content_buffer) != 0:
                self.data_dict['content'] = content_buffer

            # dbg_debug("type:{}, src:{}, dest:{}, len:{}".format(self.type, self.srcip, self.destip, self.length))
        except Exception as e:
            dbg_error(e)
            dbg_error('All Data: ', len(byte_data), byte_data)
            dbg_error('Header:   ', len(byte_data[:self._header_size]), byte_data[:self._header_size])
            dbg_error('Content:  ', len(byte_data[self._header_size:]), byte_data[self._header_size:])

            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
            # return data size to ignore errors
            return len(byte_data)

        return self.data_dict['length'] - len(byte_data)

    def toBytes(self):
        content_byte_buffer = self.content.encode('utf8')

        header_buffer = ""
        header_buffer += self.type.rjust(2)
        header_buffer += self.srcip.rjust(15)
        header_buffer += self.destip.rjust(15)
        header_buffer += (len(content_byte_buffer) + self._header_size).__str__().rjust(8)

        # reserver
        # header_buffer += ''.zfill(self._header_size - len(header_buffer))
        header_buffer += 'RESERVE'.rjust(self._header_size - len(header_buffer))
        # dbg_print('toBytes:', len(header_buffer), ',',self._header_size - len(header_buffer))
        if len(header_buffer) != self._header_size:
            dbg_error('Not fitting header size:', len(header_buffer), ',',self._header_size - len(header_buffer))
            return None

        byte_buffer = header_buffer.encode('ascii') + content_byte_buffer
        # dbg_debug("type:{}, src:{}, dest:{}, len:{}".format(self.type, self.srcip, self.destip, self.length))
        # dbg_debug('content:', len(self.content), ', ',self.content)
        # dbg_debug('toBytes:', len(byte_buffer), ', ', byte_buffer)
        return byte_buffer


    def __str__(self):
        str_buf = "type:{}, src:{}, dest:{}, len:{}, content:{}".format(self.type, self.srcip, self.destip, self.length, self.content)
        return str_buf


    @property
    def type(self):
        return self.data_dict['type']
    @type.setter
    def type(self,val):
        self.data_dict['type'] = val
    @property
    def srcip(self):
        return self.data_dict['srcip']
    @srcip.setter
    def srcip(self,val):
        self.data_dict['srcip'] = val
    @property
    def destip(self):
        return self.data_dict['destip']
    @destip.setter
    def destip(self,val):
        self.data_dict['destip'] = val
    @property
    def length(self):
        return self.data_dict['length']
    @length.setter
    def length(self,val):
        self.data_dict['length'] = val
    @property
    def content(self):
        return self.data_dict['content']
    @content.setter
    def content(self,val):
        self.data_dict['content'] = val
        self.length=len(val)
