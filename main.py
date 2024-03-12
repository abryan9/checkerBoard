import tkinter as tk
from tkinter import ttk

import time

import zoneConfig as zc

class CheckerBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.zones = ["All Zones", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "No Zone Selected"]
        self.zone = tk.StringVar()
        self.selectedZoneList = []
        
        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listRooms = tk.Listbox(self, selectmode=tk.SINGLE, yscrollcommand=self.scroll.set)
        
        self.ABS_PATH = __file__.removesuffix('main.py')
        
        self.zone_config = zc.zone_config()
        
        self.pack()
   

    def select_zone(self):
        self.zone.set("No Zone Selected")

        dropdown = tk.OptionMenu(self, self.zone, *self.zones, command=self.show_rooms)
        dropdown.pack()
        
        
        pass


    def show_clicked(self, event):
        self.label.config(text=self.zone.get())
        pass
        
        
    def show_rooms(self, zone):
        zoneDict = { 
            "All Zones": self.populate_zone(0), 
            "Zone 1": self.populate_zone(1),
            "Zone 2": self.populate_zone(2),
            "Zone 3": self.populate_zone(3),
            "Zone 4": self.populate_zone(4),
            "No Zone Selected": self.populate_zone(5),
        }
        
        print(zoneDict[zone])
        self.listRooms.delete(0, self.listRooms.size())
        self.listRooms.insert(0, *zoneDict[zone])
        self.listRooms.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scroll.config(command=self.listRooms.yview)
        pass
        
    
    def populate_zone(self, zoneNum):
    
        self.selectedZoneList = self.zone_config.get_zone(zoneNum)
            
        return self.selectedZoneList
    
    
    
    

root = tk.Tk()
root.title("CheckerBoard")
root.geometry("300x300")

checkerBoard = CheckerBoard(root)
frm = ttk.Frame(checkerBoard, padding=10)
frm.pack()

checkerBoard.select_zone()

ttk.Button(root, text="Quit", command=root.destroy).pack()
checkerBoard.mainloop()
