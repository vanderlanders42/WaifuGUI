import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"optimize": 2, "excludes": ["tkinter","html","http","lzma","urllib","wx.lib.colourutils","xml","xml.parsers","zipfile","zipimport","unittest"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#    base = "Win32GUI" 


setup(  name = "WaifuGUI",
    version = "1.2",
    description = "WaifuGUI",
    options = {"build_exe": build_exe_options},
    executables = [Executable("wgui.py", base = base, icon = "bin/prg.ico")])
