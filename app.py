#!/usr/bin/env python
import wx
import wx.grid as grid
import pandas as pd
import itertools as it

class Calculus(wx.Frame):

    ANY = "для любого"

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,600))
        self.createUI()
        self.Centre()
        self.Show(True)
        self.data = None

    def createUI(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&Файл')
        self.createMenuItem(fileMenu,self.onOpen,'&Открыть таблицу\tCtrl+O',wx.ID_ANY)
        fileMenu.AppendSeparator()
        self.createMenuItem(fileMenu,self.onQuit,'&Выход\tCtrl+Q',wx.ID_ANY)

        self.main_panel = wx.Panel(self, style=wx.SUNKEN_BORDER)

        self.top_panel = wx.Panel(self.main_panel, style=wx.SUNKEN_BORDER, size=wx.Size(1000,20))
        self.branch_list_box = wx.ComboBox(self.top_panel, style=wx.CB_READONLY, size=wx.DefaultSize, choices=[])
        self.tech_list_box = wx.ComboBox(self.top_panel, style=wx.CB_READONLY, size=wx.DefaultSize, choices=[])
        self.speed_list_box = wx.ComboBox(self.top_panel, style=wx.CB_READONLY, size=wx.DefaultSize, choices=[])

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.branch_list_box, wx.ID_ANY, wx.EXPAND | wx.ALL, border=5)
        hsizer.Add(self.tech_list_box, wx.ID_ANY, wx.EXPAND | wx.ALL, border=5)
        hsizer.Add(self.speed_list_box, wx.ID_ANY,wx.EXPAND | wx.ALL, border=5)
        self.top_panel.SetSizer(hsizer)

        self.grid = grid.Grid(self.main_panel,size=wx.Size(1000,490))
        


        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.top_panel, wx.ID_ANY, flag=wx.RIGHT | wx.EXPAND, border=5)
        vsizer.Add(self.grid, wx.ID_ANY, flag=wx.RIGHT | wx.EXPAND, border=5)
        self.main_panel.SetSizer(vsizer)
        self.main_panel.Fit()

    def createMenuItem(self,menu,function,text,id):
        item = wx.MenuItem(menu, id, text)
        menu.Append(item)
        self.Bind(wx.EVT_MENU, function, item)

    def onOpen(self, event):
        with wx.FileDialog(self, "Открыть csv файл", wildcard="files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  None

            pathname = fileDialog.GetPath()
            try:
                self.data = pd.read_csv('general.csv')   
                brnaches=self.data.branch.unique()    
                self.branch_list_box.Clear()
                self.tech_list_box.Clear()
                self.speed_list_box.Clear()
                self.widgetFiller(self.branch_list_box, brnaches,self.onSelectBranch)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    def onQuit(self, e):
        self.Close()

    def widgetFiller(self, widget, objects, function):
        """"""
        widget.Append(self.ANY)
        for obj in objects:
            widget.Append(str(obj))
        widget.Bind(wx.EVT_COMBOBOX, function)

    def onSelectBranch(self, event):
        branch = self.branch_list_box.GetStringSelection()
        print ("You selected branch: ", branch)
        if branch==self.ANY:
            self.branch_data=self.data
        else:    
            self.branch_data=self.data.query('branch=="'+branch+'"')
        self.tech_list_box.Clear()
        self.widgetFiller(self.tech_list_box, self.branch_data.technology.unique(),self.onSelectTechnology)
        print(self.branch_data)

    def onSelectTechnology(self, event):
        technology = self.tech_list_box.GetStringSelection()
        print ("You selected techology: ",  technology)
        if technology==self.ANY:
            self.technology_data=self.branch_data
        else:    
            self.technology_data=self.branch_data.query('technology=="'+technology+'"')
        self.speed_list_box.Clear()
        self.widgetFiller(self.speed_list_box, self.technology_data.speed.unique(),self.onSelectSpeed)
        print(self.technology_data)

    def onSelectSpeed(self, event):
        speed=self.speed_list_box.GetStringSelection()
        print ("You selected speed: ",  speed)
        if speed==self.ANY:
            self.speed_data=self.technology_data
        else:    
            speed=int(speed)
            self.speed_data=self.technology_data.query('speed == @speed')
        print(self.speed_data)
        self.grid.ClearGrid()
        rows=len(self.speed_data)
        cols=len(self.speed_data.columns)
        self.grid.CreateGrid(rows, cols)
        for row, col in it.product(range(len(self.speed_data)), range(len(self.speed_data.columns))):
            if col!=0:
                self.grid.SetCellValue(row, col-1, str(self.speed_data.iat[row, col]))
        self.grid.Refresh()

if __name__ == "__main__":
    app = wx.App(False)
    frame = Calculus(None, 'Калькулятор подбора тарифа')
    app.MainLoop()