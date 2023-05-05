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

#     @staticmethod
#     def fromBytes(byte_data):
#         str_buffer = byte_data.decode(encoding="utf8")

#         tmp_pkg = Package()
#         current_len = 0
#         tmp_pkg.type    = str_buffer[current_len:current_len+2]
#         current_len += 2
#         tmp_pkg.srcip   = str_buffer[current_len:current_len+15]
#         current_len += 15
#         tmp_pkg.destip  = str_buffer[current_len:current_len+15]
#         current_len += 15
#         tmp_pkg.length  = str_buffer[current_len:current_len+8]
#         tmp_pkg.content = str_buffer[64:]
#         return tmp_pkg

    def fromBytes(self, byte_data):
        str_buffer = ''
        dbg_debug('Header: ', byte_data[:64])
        current_len = 0
        try:
            str_buffer = byte_data.decode(encoding="utf8")

            # tmp_pkg = Package()
            self.data_dict['type']    = str_buffer[current_len:current_len+2].strip()
            current_len += 2
            self.data_dict['srcip']   = str_buffer[current_len:current_len+15].strip()
            current_len += 15
            self.data_dict['destip']  = str_buffer[current_len:current_len+15].strip()
            current_len += 15

            self.data_dict['length']  = int(str_buffer[current_len:current_len+8].strip())
            self.data_dict['content'] = str_buffer[64:]
            dbg_debug("type:{}, src:{}, dest:{}, len:{}".format(self.type, self.srcip, self.destip, self.length))
        except Exception as e:
            dbg_error(e)
            dbg_error(current_len, ',',str_buffer[current_len: current_len+8])

            traceback_output = traceback.format_exc()
            dbg_error(traceback_output)
            # return data size to ignore errors
            return len(byte_data)

        return self.data_dict['length'] + self._header_size - len(byte_data)


    def toBytes(self):
        str_buffer = ""
        str_buffer += self.type.rjust(2)
        str_buffer += self.srcip.rjust(15)
        str_buffer += self.destip.rjust(15)
        str_buffer += len(self.content).__str__().rjust(8)
        # reserver
        str_buffer += ''.zfill(self._header_size - len(str_buffer))
        str_buffer += self.content
        dbg_debug("type:{}, src:{}, dest:{}, len:{}".format(self.type, self.srcip, self.destip, self.length))
        return bytes(str_buffer, 'utf8')


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
