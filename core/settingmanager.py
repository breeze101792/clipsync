import tkinter as tk
from tkinter import ttk
from tkinter import font
import sys
import os
from configparser import ConfigParser

from utility.debug import *

class Setting:
    Version='0.13.0'
    class Serial:
        port = "/dev/ttyUSB0"
        baudrate = 115200
        parity = "NONE"
        stopbits = "1"
    class Log:
        path = "log"
    class Terminal:
        mode = 'normal'
        font = {
            "family"  : "",
            "size"    : 12,
            "options" : "normal"
        }
        theme = {
            "fg"        : "#E6E6E6",
            "bg"        : "#282C34",
            "cursor"    : "#606060",
            "selection" : "#357EC7",
        }
    class Profile:
        shortcut = 'shortcut.ini'
        highlight = 'highlight.ini'
    class Other:
        python = 'python'
    @staticmethod
    def createConfig(config):
        config.add_section('serial')
        config['serial']['port'] = Setting.Serial.port
        config['serial']['baudrate'] = Setting.Serial.baudrate.__str__()
        config['serial']['parity'] = Setting.Serial.parity
        config['serial']['stopbits'] = Setting.Serial.stopbits

        config.add_section('log')
        config['log']['path'] = Setting.Log.path

        config.add_section('other')
        config['other']['python'] = Setting.Other.python

        config.add_section('terminal')
        config['terminal']['font_family'] = Setting.Terminal.font['family']
        config['terminal']['font_size'] = Setting.Terminal.font['size'].__str__()
        config['terminal']['font_options'] = Setting.Terminal.font['options']
    @staticmethod
    def dumpConfig(config):
        config['serial']['port'] = Setting.Serial.port
        config['serial']['baudrate'] = Setting.Serial.baudrate.__str__()
        config['serial']['parity'] = Setting.Serial.parity
        config['serial']['stopbits'] = Setting.Serial.stopbits

        config['log']['path'] = Setting.Log.path

        config['other']['python'] = Setting.Other.python

        config['terminal']['font_family'] = Setting.Terminal.font['family']
        config['terminal']['font_size'] = Setting.Terminal.font['size'].__str__()
        config['terminal']['font_options'] = Setting.Terminal.font['options']
    @staticmethod
    def saveConfig(config, filename = 'config.ini'):
        Setting.dumpConfig(config)

        for each_cag in config:
            for each_config in config[each_cag]:
                dbg_debug(each_cag, ": ", each_config)

        with open(filename, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def readConfig(config, filename = 'config.ini'):
        Setting.createConfig(config)
        if os.path.isfile(filename):
            try:
                config.read(filename)
            except:
                pass
        Setting.Serial.port = config['serial']['port']
        Setting.Serial.baudrate = int(config['serial']['baudrate'])
        Setting.Serial.parity = config['serial']['parity']
        Setting.Serial.stopbits = config['serial']['stopbits']

        Setting.Log.path = config['log']['path']

        Setting.Other.python = config['other']['python']

        Setting.Terminal.font['family'] = config['terminal']['font_family']
        Setting.Terminal.font['size']   = int(config['terminal']['font_size'])
        Setting.Terminal.font['options'] = config['terminal']['font_options']

class SettingManager(tk.Toplevel):

    # __init__ function for class AdvcanceSetting
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        # tk.Tk.__init__(self, *args, **kwargs)
        super(SettingManager, self).__init__(*args, **kwargs)
        self.title('Advance Settings')
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.geometry("640x480")
        self.setting_config = ConfigParser()
        self.config_file = 'config.ini'
        Setting.readConfig(self.setting_config, self.config_file)

        ## Side column frame
        #################################
        # sidebar_frame = tk.Frame(self, borderwidth=1) 
        sidebar_frame = tk.Frame(self, borderwidth=1) 
        sidebar_frame.config(highlightbackground='black')
        sidebar_frame.pack(side = "left", fill='y', expand = True, padx = 5, pady = 5)

        ## button frame
        button_frame = tk.Frame(sidebar_frame) 
        button_frame.pack(side = "bottom", fill='x')

        button_apply = tk.Button(button_frame, text="Apply", command = self.applySettings)
        button_apply.pack(side = "left", padx = 3, pady = 5)

        button_apply = tk.Button(button_frame, text="Save", command = self.saveSettings)
        button_apply.pack(side = "left", padx = 3, pady = 5)

        button_cancle = tk.Button(button_frame, text="Cancle", command = self.closeWindow)
        button_cancle.pack(side = "left", padx = 3, pady = 5)

        ## page frame
        #################################
        main_frame = tk.Frame(self) 
        main_frame.pack(side = "right", fill = "both", expand = True)

        ## page frame
        #################################
        # creating a container
        # container = tk.LabelFrame(main_frame) 
        container = tk.Frame(main_frame) 
        container.pack(side = "top", fill = "both", expand = True, padx = 5, pady = 5 )

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {} 

        # iterating through a tuple consisting
        # of the different page layouts
        for each_frame in (SerialSettingFrame, TerminalSettingFrame, ThemeSettingFrame, LogSettingFrame, OtherSettingFrame):

            frame = each_frame(container, self)

            dbg_info('Sidebar Frame:', frame.pageTitle())
            self.__addSideLink(sidebar_frame, frame)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[each_frame] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(SerialSettingFrame)
        self.withdraw()

    # to display the current frame passed as
    # parameter
    def __addSideLink(self, sidebar_frame, link_frame):
        link_button = tk.Button(sidebar_frame, text=link_frame.pageTitle(), command = lambda : self.show_frame(type(link_frame)), borderwidth=0, anchor=tk.NW)
        link_button.pack(side = "top", fill='x')
    def show_frame(self, cont):
        frame = self.frames[cont]
        dbg_debug('Raise ', frame.pageTitle())
        frame.tkraise()
    def openWindow(self):
        self.refreshSettings()
        self.deiconify()
    def closeWindow(self):
        self.withdraw()
    def saveSettings(self):
        dbg_info('Save Settings')
        for each_frame in self.frames:
            self.frames[each_frame].applySetting()
        Setting.saveConfig(self.setting_config, self.config_file)
        self.withdraw()
    def applySettings(self):
        dbg_info('Apply Settings')
        for each_frame in self.frames:
            self.frames[each_frame].applySetting()
    def refreshSettings(self):
        dbg_info('Refresh Settings')
        for each_frame in self.frames:
            self.frames[each_frame].refreshSetting()

class PageFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        tk.LabelFrame.__init__(self, parent)
        self['text'] = 'Template'
    def pageTitle(self):
        return self['text']
    def applySetting(self):
        pass
    def refreshSetting(self):
        pass

class LogSettingFrame(PageFrame):
    def __init__(self, *args, **kwargs):
        super(LogSettingFrame, self).__init__(*args, **kwargs)
        self['text'] = 'Log'

        # self.window.geometry("220x60")
        # if os.name == 'nt':
        #     Setting.Log.path = '.\log'
        # else:
        #     Setting.Log.path = './log'

        # ui vars
        self.ui_path = tk.StringVar(value = Setting.Log.path)

        ## Log setting
        #############################3
        log_frame = self
        grid_row_count = 0
        log_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(1, weight=2)

        # seria dev
        path_label = tk.Label(log_frame,text="Path: ")
        path_entry = tk.Entry(log_frame, textvariable = self.ui_path)

        path_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        path_entry.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)

    def applySetting(self):
        dbg_info('Apply Setting: ')
        Setting.Log.path = self.ui_path.get()

class TerminalSettingFrame(PageFrame):
    def __init__(self, *args, **kwargs):
        super(TerminalSettingFrame, self).__init__(*args, **kwargs)
        self['text'] = 'Terminal(C)'

        # vars
        fonts=list(font.families())
        fonts.sort()

        # ui vars
        self.ui_mode = tk.StringVar(value = Setting.Terminal.mode)
        if Setting.Terminal.font['family'] not in fonts:
            if "Source Code Pro" in fonts:
                Setting.Terminal.font['family'] = "Source Code Pro"
            elif "Consolas" in fonts:
                Setting.Terminal.font['family'] = "Consolas"
            elif "Monaco" in fonts:
                Setting.Terminal.font['family'] = "Monaco"
        self.ui_font = tk.StringVar(value = Setting.Terminal.font['family'])
        self.ui_font_size = tk.StringVar(value = Setting.Terminal.font['size'])

        ## Terminal setting
        #############################3
        term_frame = self
        grid_row_count = 0
        term_frame.columnconfigure(0, weight=1)
        term_frame.columnconfigure(1, weight=2)

        # Terminal mode
        mode_label = tk.Label(term_frame,text="Terminal Mode(fast/raw): ")
        mode_entry = tk.Entry(term_frame, textvariable = self.ui_mode)

        mode_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        mode_entry.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

        # Theme
        ## Font
        font_label = tk.Label(term_frame,text="Font: ")
        font_combo = ttk.Combobox(term_frame, width = 17, textvariable=self.ui_font)
        font_combo["values"] = fonts
        font_combo["state"] = "readonly"
        font_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        font_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

        # font size
        font_size_label = tk.Label(term_frame,text="Font size: ")
        font_size_entry = tk.Entry(term_frame, textvariable = self.ui_font_size)
        font_size_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        font_size_entry.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

    def applySetting(self):
        dbg_info('Apply Setting: ')
        Setting.Terminal.mode = self.ui_mode.get()
        Setting.Terminal.font['family'] = self.ui_font.get()
        Setting.Terminal.font['size'] = self.ui_font_size.get()

class OtherSettingFrame(PageFrame):
    def __init__(self, *args, **kwargs):
        super(OtherSettingFrame, self).__init__(*args, **kwargs)
        self['text'] = 'Other'
        # ui vars
        self.ui_python_exec = tk.StringVar(value = Setting.Other.python)

        ## Terminal setting
        #############################3
        other_frame = self
        grid_row_count = 0
        other_frame.columnconfigure(0, weight=1)
        other_frame.columnconfigure(1, weight=2)

        mode_label = tk.Label(other_frame,text="Python Exec Path: ")
        mode_entry = tk.Entry(other_frame, textvariable = self.ui_python_exec)

        mode_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        mode_entry.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

    def applySetting(self):
        dbg_info('Apply Setting: ')
        Setting.Other.python = self.ui_python_exec.get()

class ThemeSettingFrame(PageFrame):
    def __init__(self, *args, **kwargs):
        super(ThemeSettingFrame, self).__init__(*args, **kwargs)
        self['text'] = 'Theme(C)'
        # ui vars
        self.ui_python_exec = tk.StringVar(value = Setting.Other.python)

        ## Theme setting
        #############################3
        theme_frame = self
        grid_row_count = 0
        theme_frame.columnconfigure(0, weight=1)
        theme_frame.columnconfigure(1, weight=2)

        # Tkinter Theme
        self.tk_style = ttk.Style()
        self.ui_theme = tk.StringVar(value = self.tk_style.theme_use())
        theme_label = tk.Label(theme_frame,text="Theme: ")
        theme_combo = ttk.Combobox(theme_frame, width = 17, textvariable=self.ui_theme)
        theme_combo["values"] = self.tk_style.theme_names()
        theme_combo["state"] = "readonly"
        theme_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        theme_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

    def applySetting(self):
        dbg_info('Apply Setting: ')
        self.tk_style.theme_use(self.ui_theme.get())

from console.serialconsole import *
class SerialSettingFrame(PageFrame):
    def __init__(self, *args, **kwargs):
        super(SerialSettingFrame, self).__init__(*args, **kwargs)
        self['text'] = 'Serial'

        # ui vars
        # dbg_debug(SerialConsole.getList())
        if len(SerialConsole.getList()) >= 1:
            Setting.Serial.port = SerialConsole.getList()[0]
        else:
            Setting.Serial.port = ''

        self.ui_device = tk.StringVar(value = Setting.Serial.port)
        self.ui_baudrate = tk.IntVar(value = Setting.Serial.baudrate)
        self.ui_parity = tk.StringVar(value = Setting.Serial.parity)
        self.ui_stopbits = tk.StringVar(value = Setting.Serial.stopbits)

        ## serial setting
        #############################3
        # a frame contains COM's information, and start/stop button
        setting_frame = self
        setting_frame.columnconfigure(0, weight=1)
        setting_frame.columnconfigure(1, weight=2)
        grid_row_count = 0

        # seria dev
        port_label = tk.Label(setting_frame,text="Port: ")
        port_entry = tk.Entry(setting_frame, textvariable = self.ui_device)

        self.port_combo = ttk.Combobox(setting_frame, width = 17, textvariable=self.ui_device)
        self.port_combo["values"] = SerialConsole.getList()
        # self.port_combo["state"] = "readonly"

        port_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        self.port_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        # port_entry.grid(row = 1, column = 2, padx = 5, pady = 3)
        grid_row_count += 1

        # Baudrate
        baudrate_label = tk.Label(setting_frame,text="Baudrate: ")
        baudrate_combo = ttk.Combobox(setting_frame, width = 17, textvariable=self.ui_baudrate)
        baudrate_combo["values"] = ("1800","2400","4800","9600","19200","28800","38400","57600","76800","115200","230400","460800","576000","921600","1500000")
        baudrate_combo["state"] = "readonly"
        baudrate_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        baudrate_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

        # parity
        parity_label = tk.Label(setting_frame,text="Parity: ")
        parity_combo = ttk.Combobox(setting_frame, width = 17, textvariable=self.ui_parity)
        parity_combo["values"] = ("NONE","ODD","EVEN","MARK","SPACE")
        parity_combo["state"] = "readonly"
        parity_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        parity_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

        # stop bit
        stopbit_label = tk.Label(setting_frame,text="Stopbits: ")
        stopbit_combo = ttk.Combobox(setting_frame, width = 17, textvariable=self.ui_stopbits)
        stopbit_combo["values"] = ("1","1.5","2")
        stopbit_combo["state"] = "readonly"
        stopbit_label.grid(row = grid_row_count, column = 0, padx = 5, pady = 3, sticky=tk.W)
        stopbit_combo.grid(row = grid_row_count, column = 1, padx = 5, pady = 3, sticky=tk.E)
        grid_row_count += 1

    def applySetting(self):
        dbg_info('Apply Setting: ')
        Setting.Serial.port = self.ui_device.get()
        Setting.Serial.baudrate =self.ui_baudrate.get()
        Setting.Serial.parity = self.ui_parity.get()
        Setting.Serial.stopbits = self.ui_stopbits.get()
        dbg_debug('Uart info: ', Setting.Serial.port, ', ', Setting.Serial.baudrate, ', ', Setting.Serial.parity, ', ', Setting.Serial.stopbits,'')
    def refreshSetting(self):
        self.port_combo["values"] = SerialConsole.getList()
