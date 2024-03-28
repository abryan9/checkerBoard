import tkinter as tk
from tkinter import ttk, font
from datetime import datetime, timedelta

# import time

import zoneConfig as zc

class CheckerBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        frame = tk.Frame(master)
        
        self.zones = ["All Zones", "Zone 1", "Zone 2", "Zone 3", "Zone 4", "No Zone Selected"]
        self.zone = tk.StringVar()
        self.zone.set('No Zone Selected')
        
        self.select_zone()
        self.zone_config = zc.zone_config()
        
        currentTime = datetime.now()
        currentDelta = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=int(currentTime.second))
        self.checkedTime = tk.StringVar()
        self.checkedTime.set(f'Last Updated: {currentDelta}')
        self.timeLabel = tk.Label(frame, textvariable=self.checkedTime)
        self.timeLabel.configure(bg='#cbcccd')
        self.timeLabel.pack_propagate(False)
        self.timeLabel.pack(side=tk.TOP, anchor=tk.W, expand=0)
        
        self.yscroll = tk.Scrollbar(frame)
        self.yscroll.configure(bg='#cbcccd')
        self.yscroll.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, pady=(0,40))
        self.listRooms = tk.Listbox(frame, height=int(master.winfo_height()/25), yscrollcommand=self.yscroll.set)
        self.listRooms.configure(bg='#cbcccd')
        self.listRooms.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH, expand=1, pady=(0,10))
        
        tk.Button.configure(self, bg='#cbcccd')
        tk.Button(frame, text='Quit', command=root.destroy).pack(side=tk.RIGHT, anchor=tk.S, padx=(1,0))
        tk.Button(frame, text='Save').pack(side=tk.RIGHT, anchor=tk.S, padx=(1,0))
        tk.Button(frame, text='Refresh', command=self.refresh).pack(side=tk.RIGHT, anchor=tk.E, padx=(1,0))
        
        self.ABS_PATH = __file__.removesuffix('main.py')
        
        self.pack(fill=tk.BOTH, expand=1)
        
        frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=1)
        
        return None
    
    
    def set_list_height(self, passedHeight):
        # print(passedHeight)
        self.listRooms.config(height=int(passedHeight/25.5))
        return 0
   

    def select_zone(self):
        self.zone.set('No Zone Selected')

        dropdown = tk.OptionMenu(self, self.zone, *self.zones, command=self.show_rooms)
        dropdown.configure(bg='#cbcccd')
        dropdown.pack_propagate(False)
        dropdown.pack(side=tk.TOP, anchor=tk.N, expand=0)
        return 0


    def refresh(self):
        self.get_zone_list(str(self.zone))
        return 0
    
    
    def get_zone_list(self, zone='No Zone Selected'):
    
        currentTime = datetime.now()
        currentDelta = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=int(currentTime.second))
        self.checkedTime.set(f'Last Updated: {currentDelta}')
        
        if zone[:2] != 'No':
            if zone == 'All Zones':
                zoneNum = 0
            else:
                zoneNum = int(zone[-1])
            return self.zone_config.get_zone(zoneNum)
        else:
            return ['']
    
    
    def show_rooms(self, zone):
    
        rawZoneList = self.get_zone_list(zone)
        
        self.listRooms.delete(0, tk.END)
        self.listRooms.insert(0, *rawZoneList)
        self.listRooms.config(bg='#cbcccd')
        self.listRooms.pack(side=tk.TOP, fill=tk.X, anchor=tk.N, expand=1)
        self.yscroll.config(bg='#cbcccd', command=self.listRooms.yview)
        
        for item in range(len(rawZoneList)):
            if 'UNAVAILABLE' in str(self.listRooms.get(item)):
                self.listRooms.itemconfig(item,{'bg':'#77160c', 'fg':'#ebeced'})
            else:
                self.listRooms.itemconfig(item,{'bg':'#525a62', 'fg':'#ebeced'})
        
        return 0


root = tk.Tk()
root.title('CheckerBoard')
root.geometry('750x630')
root.option_add('*Font', 'consolas 12')
root.config(bg='#cbcccd')
root.update_idletasks()
checkerBoard = CheckerBoard(root)

def onResize(event):
    root.config(width=event.width, height=event.height)
    checkerBoard.set_list_height(root.winfo_height())
    
root.bind('<Configure>', onResize)

# checkerBoard.bind('<Configure>', onResize)

checkerBoard.mainloop()
