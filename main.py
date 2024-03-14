import tkinter as tk
from tkinter import ttk

import time

import zoneConfig as zc

class CheckerBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        frame = tk.Frame(master)
        
        self.zones = ["All Zones", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "No Zone Selected"]
        self.zone = tk.StringVar()
        
        self.select_zone()
        
        tk.Label(frame, text='test').pack(side=tk.TOP, fill=tk.X, anchor=tk.N, expand=0)
        
        self.yscroll = tk.Scrollbar(frame)
        self.yscroll.pack(side=tk.LEFT, anchor=tk.E, fill=tk.Y, pady=(0,25))
        self.listRooms = tk.Listbox(frame, yscrollcommand=self.yscroll.set)
        self.listRooms.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH, expand=1, pady=(0,10))
        
        self.ABS_PATH = __file__.removesuffix('main.py')
        
        self.zone_config = zc.zone_config()
        
        self.pack(fill='both', expand=1)
        
        tk.Button(frame, text='Quit', command=root.destroy).pack(side=tk.RIGHT, anchor=tk.E, padx=(1,0))
        tk.Button(frame, text='Save').pack(side=tk.RIGHT, anchor=tk.E, padx=(1,0))
        tk.Button(frame, text='Refresh').pack(side=tk.RIGHT, anchor=tk.E, padx=(1,0))
        
        frame.pack(fill='both', padx=10, pady=10, expand=1)
   

    def select_zone(self):
        self.zone.set('No Zone Selected')

        dropdown = tk.OptionMenu(self, self.zone, *self.zones, command=self.show_rooms)
        dropdown.pack(side=tk.TOP, anchor=tk.N, expand=0)
        
        
        pass


    def show_clicked(self, event):
        frame.label.config(text=self.zone.get())
        pass
    
    
    def get_zone_list(self, zone):
        
        if zone[:2] != 'No':
            if zone == 'All Zones':
                zoneNum = 0
            else:
                zoneNum = int(zone[-1])
            return self.zone_config.get_zone(zoneNum)
        else:
            return ['']
    
    
    def show_rooms(self, zone):
        
        self.listRooms.delete(0, tk.END)
        self.listRooms.insert(0, *self.get_zone_list(zone))
        self.listRooms.pack(side=tk.TOP, fill='both', expand=1)
        self.yscroll.config(command=self.listRooms.yview)
        pass


root = tk.Tk()
root.title('CheckerBoard')
root.geometry('500x300')

checkerBoard = CheckerBoard(root)

checkerBoard.mainloop()
