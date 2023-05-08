import sys
import os
import inspect
from configparser import ConfigParser
# from utility.debug import *

class Config:
    version='0.1.0'
    program_name = 'Config Manager'
    def __init__(self):
        pass
    class Server:
        ip = "0.0.0.0"
        port = 11320
    class Debug:
        log_level = "information"

class ConfigManager:
    def initialize(self, cfg):
        pass
    def dump(self, instance, indent=''):
        indent_unit = 2 * ' '
        title_width = 20 - len(indent)

        ins_dict = vars(instance)
        for each_key in ins_dict.keys():
            if each_key.startswith('_') is not True and type(ins_dict[each_key]).__name__  != 'function':
                if inspect.isclass(ins_dict[each_key]):
                    print('{}[{}]'.format(indent, each_key))
                    self.dump(ins_dict[each_key], indent + indent_unit)
                else:
                    print('{}{}: {}'.format(indent, each_key.ljust(title_width), ins_dict[each_key]))
    def dict(self, instance, indent=''):
        indent_unit = 2 * ' '
        title_width = 20 - len(indent)

        ins_dict = vars(instance)
        ret_dict = dict()
        for each_key in ins_dict.keys():
            if each_key.startswith('_') is not True and type(ins_dict[each_key]).__name__  != 'function':
                if inspect.isclass(ins_dict[each_key]):
                    print('{}[{}]'.format(indent, each_key))
                    ret_dict[each_key] = self.dict(ins_dict[each_key], indent + indent_unit)
                else:
                    print('{}{}: {}'.format(indent, each_key.ljust(title_width), ins_dict[each_key]))
                    ret_dict[each_key] = ins_dict[each_key]
        return ret_dict

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # @staticmethod
    # def createConfig(config):
    #     config.add_section('serial')
    #     config['serial']['port'] = Setting.Serial.port
    #     config['serial']['baudrate'] = Setting.Serial.baudrate.__str__()
    #     config['serial']['parity'] = Setting.Serial.parity
    #     config['serial']['stopbits'] = Setting.Serial.stopbits

    #     config.add_section('log')
    #     config['log']['path'] = Setting.Log.path

    #     config.add_section('other')
    #     config['other']['python'] = Setting.Other.python

    #     config.add_section('terminal')
    #     config['terminal']['font_family'] = Setting.Terminal.font['family']
    #     config['terminal']['font_size'] = Setting.Terminal.font['size'].__str__()
    #     config['terminal']['font_options'] = Setting.Terminal.font['options']
    # @staticmethod
    # def dumpConfig(config):
    #     config['serial']['port'] = Setting.Serial.port
    #     config['serial']['baudrate'] = Setting.Serial.baudrate.__str__()
    #     config['serial']['parity'] = Setting.Serial.parity
    #     config['serial']['stopbits'] = Setting.Serial.stopbits

    #     config['log']['path'] = Setting.Log.path

    #     config['other']['python'] = Setting.Other.python

    #     config['terminal']['font_family'] = Setting.Terminal.font['family']
    #     config['terminal']['font_size'] = Setting.Terminal.font['size'].__str__()
    #     config['terminal']['font_options'] = Setting.Terminal.font['options']
    # @staticmethod
    # def saveConfig(config, filename = 'config.ini'):
    #     Setting.dumpConfig(config)

    #     for each_cag in config:
    #         for each_config in config[each_cag]:
    #             dbg_debug(each_cag, ": ", each_config)

    #     with open(filename, 'w') as configfile:
    #         config.write(configfile)

    # @staticmethod
    # def readConfig(config, filename = 'config.ini'):
    #     Setting.createConfig(config)
    #     if os.path.isfile(filename):
    #         try:
    #             config.read(filename)
    #         except:
    #             pass
    #     Setting.Serial.port = config['serial']['port']
    #     Setting.Serial.baudrate = int(config['serial']['baudrate'])
    #     Setting.Serial.parity = config['serial']['parity']
    #     Setting.Serial.stopbits = config['serial']['stopbits']

    #     Setting.Log.path = config['log']['path']

    #     Setting.Other.python = config['other']['python']

    #     Setting.Terminal.font['family'] = config['terminal']['font_family']
    #     Setting.Terminal.font['size']   = int(config['terminal']['font_size'])
    #     Setting.Terminal.font['options'] = config['terminal']['font_options']


if __name__ == "__main__":
    cfgmgr = ConfigManager()
    # cfgmgr.dump(Config)
    print(cfgmgr.dict(Config))
