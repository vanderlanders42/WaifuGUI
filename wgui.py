# coding: utf-8
import wx
from subprocess import run
from threading import Thread
from colorama import Fore, Back, Style, init

#WaifuGUI (A waifu-converter-cpp interface)
#Version 1.3
#Copyright 2018 Vladimir Vanderlanders
"""This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""
#Attention, commentaires en Franglais.

#Init
init()
print (Fore.BLACK + Back.WHITE + "WaifuGUI 1.3 Output System" + Style.RESET_ALL)
print (Fore.BLACK + Back.WHITE + "2018 Vladimir Vanderlanders" + Style.RESET_ALL)
print (Fore.YELLOW + "\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n" + Style.RESET_ALL)
                
class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title = title,size = (505,250), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        pnl = wx.Panel(self)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("bin/prg.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        #Barre de menu
        self.BarreMenu()

        textecon0  = wx.StaticText(pnl, 1, "Processing Settings :", pos = (5, 2)) 
        #Zoom
        textecon1 = wx.StaticText(pnl, 1, "Zoom :     x",pos = (44, 21)) 
        self.s_zoom = wx.Slider (pnl, value=1, minValue=1, maxValue=20, pos = (40, 21), style=wx.SL_VALUE_LABEL)
        
        #Noise reduction
        textecon2 = wx.StaticText(pnl, 1, "Noise Reduction :",pos = (150, 21))
        self.s_nr = wx.Slider (pnl, value=0, minValue=0, maxValue=3, pos = (200, 21), style=wx.SL_VALUE_LABEL)

        gandalf1 = wx.StaticLine(pnl, 1, (0, 61), (600, 2), style=wx.LI_HORIZONTAL)

        #Input path
        textecon3 = wx.StaticText(pnl, 1, "Input :", pos = (9, 71))
        self.input_dir_ctrl = wx.DirPickerCtrl(pnl, pos = (52, 67), size = (290, -1))
        #Output path
        textecon4 = wx.StaticText(pnl, 1, "Output :", pos = (4, 101))
        self.output_dir_ctrl = wx.DirPickerCtrl(pnl, pos = (52, 97), size = (290, -1))

        gandalf2 = wx.StaticLine(pnl, 1, (0, 127), (600, 2), style=wx.LI_HORIZONTAL)

        #Launch button
        start_b = wx.Button(pnl, 1, "Fire !", (94, 135), (150, 25))
        start_b.Bind(wx.EVT_BUTTON,self.OnStart)

        #Barre d'état
        self.CreateStatusBar()
        self.SetStatusText("Ready to drop the bass.")

        gandalf3 = wx.StaticLine(pnl, 1, (358, 0), (2, 360), style=wx.LI_VERTICAL)

        #Block size parameters
        textecon5 = wx.StaticText(pnl, 1, "Block Size :",pos = (375, 21))
        self.s_block = wx.TextCtrl (pnl, value="128", pos = (435, 17), size = (35, -1))

        #Processor parameters
        textecon6 = wx.StaticText(pnl, 1, "Processor :",pos = (375, 71))
        self.s_cpu = wx.TextCtrl (pnl, value="0", pos = (435, 67), size = (35, -1))
        list_b = wx.Button(pnl, 1, "List", (379, 97))
        list_b.Bind(wx.EVT_BUTTON,self.OnList)

        #Size optimizer
        opt = wx.Button(pnl, 1, "Optimize !", (379, 135))
        opt.Bind(wx.EVT_BUTTON,self.OnOpt)
        

    def BarreMenu(self):

        fileMenu = wx.Menu()
        
        exitItem = fileMenu.Append(-1, "&Exit\tCtrl-D",
                "Tired already ?")
        
        helpMenu = wx.Menu()
        
        aboutItem = helpMenu.Append(1, "&About...\t",
                "About WaifuGUI")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&?")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        #Ferme le programme.
        self.Close(True)

    def OnAbout(self, event):
        """A propos"""
        wx.MessageBox("WaifuGUI Version 1.3\nA waifu-converter-cpp interface.\n2018 Vladimir Vanderlanders\n\nUnder GPL 2 License",
                      "About WaifuGUI",
                      wx.OK|wx.ICON_INFORMATION)

    def OnList(self, event):
        arguments = ["bin/waifu2x-converter-cpp", "--list-processor"]
        session = waifu(arguments,self)
        session.start()

    def OnStart(self, event):
	#Collecte des informations...
        ratio = "--scale_ratio " + str(self.s_zoom.GetValue())
        input_dir = "-i " + self.input_dir_ctrl.GetPath()
        output_dir = "-o " + self.output_dir_ctrl.GetPath()
        if self.s_nr.GetValue() == 0:
            mode = "-m scale"
            nr = ""
        else :
            mode = "-m noise_scale"
            nr = "--noise_level " + str(self.s_nr.GetValue())
        block = "--block_size " + self.s_block.GetLineText(0)
        proco = "--processor " + self.s_cpu.GetLineText(0)
            
	#Rassemblement national lol
        arguments = ["bin/waifu2x-converter-cpp", block, proco, "-q", ratio, nr, mode, input_dir, output_dir]
        #print(arguments)
        
        global session	
        session = waifu(arguments,self)
        session.start()

    def OnOpt(self,event):
        arguments = ["bin/pngopt"]
        run(arguments, shell=False)

#Classe chargé de lancer un thread séparé pour waifu-converter-cpp.
class waifu(Thread):

    def __init__(self,arg,out):
        Thread.__init__(self)
        self.arguments = arg
        self.out = out
        
    def run(self):
        self.out.SetStatusText("\nWait for it...")
        print(Fore.BLACK + Back.WHITE + "Output :" + Style.RESET_ALL)
        
        #Le lancement, c'est maintenant !
        run(self.arguments, shell=False)
        print(Fore.BLACK + Back.GREEN + "*Break*" + Style.RESET_ALL)
        self.out.SetStatusText("\nReady !")

app = wx.App()
frm = MainFrame(None, title='WaifuGUI')
frm.Show()
app.MainLoop()
