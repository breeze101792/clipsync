import time
import json
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

    @staticmethod
    def fromBytes(byte_data):
        byte_buf = byte_data.decode(encoding="utf-8", errors="strict")
        tmp_json = json.loads(byte_buf)

        tmp_pkg = Package()
        tmp_pkg.type    = tmp_json['type']
        tmp_pkg.srcip   = tmp_json['srcip']
        tmp_pkg.destip  = tmp_json['destip']
        tmp_pkg.length  = tmp_json['length']
        tmp_pkg.content = tmp_json['content']
        dbg_debug(tmp_pkg)
        return tmp_pkg
    def __str__(self):
        str_buf = "type:{}, src:{}, dest:{}, len:{}, content:{}".format(self.type, self.srcip, self.destip, self.length, self.content)
        return str_buf


    def toBytes(self):
        tmp_json = json.dumps(self.data_dict, indent=2)
        byte_buf = tmp_json.__str__().encode()
        return byte_buf

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
