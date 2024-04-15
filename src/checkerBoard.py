import tkinter as tk
from tkinter import font
from datetime import date, datetime, timedelta
import time
import pandas as pd
import os
import json

class CheckerBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.frame = tk.Frame(master)
        self.frame.pack(expand=1)
        self.header = tk.Frame(self.frame)
        self.boxes = tk.Frame(self.frame)
        self.buttons = tk.Frame(self.frame)
        
        self.zones = ['All Zones', 'Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'No Zone Selected']
        self.zone = tk.StringVar()
        self.zone.set('No Zone Selected')
        
        self.select_zone()
        self.zone_config = zone_config()
        
        self.colorPallete = {
            'UW Gold': '#ffc425',
            'UW Brown': '#492f24',
            'Charcoal': '#575a62',
            'Slate': '#79706c',
            'Prairie Grass': '#7e7615',
            'Spring Leaves': '#a2a42c',
            'Canyon Rock': '#874917',
            'Cowboy Boot': '#9a651e',
            'Indian Paintbrush': '#77160c',
            'Evening Sky': '#2a3e60',
            'Cool Grey 3': '#cbcccd',
            'Cool Grey 1': '#ebeced',
            'Light Beige': '#d4cbc6',
        }
        
        currentTime = datetime.now()
        currentDelta = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=int(currentTime.second))
        self.checkedTime = tk.StringVar()
        self.checkedTime.set(f'Last Updated: {currentDelta}')
        self.timeLabel = tk.Label(self.header, textvariable=self.checkedTime)
        # self.timeLabel.configure(bg='#cbcccd', bd=0)
        self.timeLabel.pack_propagate(False)
        self.timeLabel.pack(side=tk.LEFT, anchor=tk.E)
        
        self.yscroll = tk.Scrollbar(self.boxes, orient='vertical', command=self.onVsb)
        # self.yscroll.configure(bg='#cbcccd')
        self.yscroll.pack(side=tk.LEFT, fill=tk.Y, expand=0)
        
        self.listRooms = tk.Listbox(self.boxes, width=9, height=10, yscrollcommand=self.onMouseWheel)
        # self.listRooms.configure(height=root.winfo_height()-100)
        self.listRooms.pack(side=tk.LEFT, expand=0)
        
        self.listDates = tk.Listbox(self.boxes, width=12, height=10, yscrollcommand=self.onMouseWheel)
        self.listDates.pack(side=tk.LEFT, expand=0)
        
        self.listNeedsChecked = tk.Listbox(self.boxes, width=4, height=10, yscrollcommand=self.onMouseWheel)
        self.listNeedsChecked.pack(side=tk.LEFT, expand=0)

        self.listAvailable = tk.Listbox(self.boxes, width=25, height=10, yscrollcommand=self.onMouseWheel)
        self.listAvailable.pack(side=tk.LEFT, expand=0)

        self.listComments = tk.Listbox(self.boxes, height=10, yscrollcommand=self.yscroll.set)
        self.listComments.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, expand=1)

        self.listRooms.bind('<MouseWheel>', self.onMouseWheel)
        self.listDates.bind('<MouseWheel>', self.onMouseWheel)
        self.listNeedsChecked.bind('<MouseWheel>', self.onMouseWheel)
        self.listAvailable.bind('<MouseWheel>', self.onMouseWheel)
        self.listComments.bind('<MouseWheel>', self.onMouseWheel)
        
        # tk.Button.configure(self.buttons, bg='#cbcccd')
        tk.Button(self.buttons, text='Quit', command=root.destroy).pack(side=tk.RIGHT, anchor=tk.S)
        tk.Button(self.buttons, text='Save').pack(side=tk.RIGHT, anchor=tk.S)
        tk.Button(self.buttons, text='Refresh', command=self.refresh).pack(side=tk.RIGHT, anchor=tk.S)
        
        self.header.pack(side=tk.TOP, fill=tk.X, expand=1, pady=4, padx=4)
        self.boxes.pack(side=tk.TOP, fill=tk.X, expand=0, padx=4)
        self.buttons.pack(side=tk.TOP, fill=tk.X, expand=1, pady=4, padx=4)
        
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        
        
        return None
    
    
    def onVsb(self, *args):
        self.listRooms.yview(*args)
        self.listDates.yview(*args)
        self.listNeedsChecked.yview(*args)
        self.listAvailable.yview(*args)
        self.listComments.yview(*args)
    
    
    def onMouseWheel(self, *args):
        try:
            convertedArgs = list(float(arg) for arg in args)
            self.yscroll.set(convertedArgs[0], convertedArgs[-1])
            self.listRooms.yview('moveto', args[0])
            self.listDates.yview('moveto', args[0])
            self.listNeedsChecked.yview('moveto', args[0])
            self.listAvailable.yview('moveto', args[0])
            self.listComments.yview('moveto', args[0])
        except:
            pass
    
    
    def set_list_size(self, newHeight, newWidth):
        offset=6
        self.listRooms.configure(height=int(newHeight/19.04)-offset)
        self.listDates.configure(height=int(newHeight/19.04)-offset)
        self.listNeedsChecked.configure(height=int(newHeight/19.04)-offset)
        self.listAvailable.configure(height=int(newHeight/19.04)-offset)
        self.listComments.configure(height=int(newHeight/19.04)-offset, width=int(newWidth/19.04))
        return 0


    def select_zone(self):
        # self.zone.set('No Zone Selected')

        dropdown = tk.OptionMenu(self.header, self.zone, *self.zones, command=self.show_rooms)
        # dropdown.configure(bg='#cbcccd')
        dropdown.pack_propagate(False)
        dropdown.pack(side=tk.TOP)
        return 0


    def refresh(self):
        self.get_zone_dict(str(self.zone))
        return 0
    
    
    def clear_tree(self):
        for item in self.listTree.get_children():
            self.listTree.delete(item)
    
    
    def get_zone_dict(self, zone='No Zone Selected'):
    
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
    
        rawZoneDict = self.get_zone_dict(zone)
        
        self.listRooms.delete(0, tk.END)
        self.listDates.delete(0, tk.END)
        self.listNeedsChecked.delete(0, tk.END)
        self.listAvailable.delete(0, tk.END)
        self.listComments.delete(0, tk.END)
        
        self.yscroll.config(command=self.listRooms.yview)
        
        try:
        
            for item in rawZoneDict.keys():
                self.listRooms.insert(tk.END, item)
                self.listDates.insert(tk.END, rawZoneDict[item]['Last Checked'])
                
                self.listNeedsChecked.insert(tk.END, rawZoneDict[item]['Needs Checked'])
                if rawZoneDict[item]['Needs Checked'] == 'YES':
                    self.listNeedsChecked.itemconfig(tk.END, {'bg':self.colorPallete['UW Brown'], 'fg':self.colorPallete['Cool Grey 1']})
                else:
                    self.listNeedsChecked.itemconfig(tk.END, {'bg':self.colorPallete['UW Gold']})
            
                self.listAvailable.insert(tk.END, rawZoneDict[item]['Available'])
                if 'UNAVAILABLE' not in rawZoneDict[item]['Available']:
                    self.listAvailable.itemconfig(tk.END, {'bg':self.colorPallete['Evening Sky'], 'fg':self.colorPallete['Cool Grey 1']})
                else:
                    self.listAvailable.itemconfig(tk.END, {'bg':self.colorPallete['Indian Paintbrush'], 'fg':self.colorPallete['Cool Grey 1']})
                
                self.listComments.insert(tk.END, rawZoneDict[item]['Comments'])
            
        except:
            pass
            
        self.listRooms.pack(side=tk.LEFT, expand=0)
        self.listDates.pack(side=tk.LEFT, expand=0)
        self.listNeedsChecked.pack(side=tk.LEFT, expand=0)
        self.listAvailable.pack(side=tk.LEFT, expand=0)
        self.listComments.pack(side=tk.LEFT, fill=tk.X, expand=1)
        
        return 0
    
    
    def show_full_schedule(self, event):
        print('Right Mouse Clicked!')
        pass


    def highlight_boxes(self, event):
        listboxes = [self.listRooms, self.listDates, self.listNeedsChecked, self.listAvailable, self.listComments]
        storedClick = 0
        for listbox in listboxes:
            try:
                storedClick += listbox.curselection()[0]
            except:
                pass
        
        self.show_rooms(self.zone.get())
        
        for listbox in listboxes:
            try:
                listbox.itemconfig(storedClick, {'bg':self.colorPallete['Charcoal'], 'fg':self.colorPallete['Cool Grey 1']})
            except:
                pass
     
        self.listRooms.pack(side=tk.LEFT, expand=0)
        self.listDates.pack(side=tk.LEFT, expand=0)
        self.listNeedsChecked.pack(side=tk.LEFT, expand=0)
        self.listAvailable.pack(side=tk.LEFT, expand=0)
        self.listComments.pack(side=tk.LEFT, fill=tk.X, expand=1)
        return 0


class zone_config():
    
    allBuildings = '''
        SI STEM EERB AN BC HS GE ES EIC
        EN AG EA ED HA HI BU
        CR PS AS BS NAC RH HO
        PA FA CB LS AB AC VA
        '''

    def __init__(self):
        self.load_zones = self.pull_zones()


    def get_zone(self, zoneNum):
        zoneList = [
            self.allBuildings,
            'SI STEM EERB AN BC HS GE ES EIC',
            'EN AG EA ED HA HI BU',
            'CR PS AS BS NAC RH HO',
            'PA FA CB LS AB AC VA',
        ]
        
        roomDict = {}
        for room in self.load_zones.keys():
            roomDictDict = {}
            if room.split(" ")[0] in zoneList[zoneNum]:
                available = self.check_availability(self.load_zones[room])
                roomDictDict.update({'Last Checked': '10/10/1010', 'Needs Checked': 'NO', 'Available': str(available), 'Comments': ''})
                roomDict.update({room: roomDictDict})
        return roomDict

    
    def pull_zones(self):
        roomsDict = {}
        
        if os.path.exists(ABS_PATH + 'rooms.json'):
            config = open(ABS_PATH + 'rooms.json', 'r')
            roomsDict = json.load(config)
            
        else:
            roomsDict = self.generate_config()
    
        return roomsDict
    

    def generate_config(self):
        data = (ABS_PATH + 'roomConfig.csv')
        loadedData = pd.read_csv(data, names=['Rooms', 'Times', 'Contact', 'Empty'], engine='pyarrow', header=None)
        roomFile = open(ABS_PATH + 'rooms.json', 'w')
        
        rows, columns = loadedData.shape
        
        roomDict = {}
        currentRoom = 'AB 103'
        tempList = []
        roomFile.write('{\n')
        for row in range(rows):
            search = loadedData.loc[row, 'Rooms']
            if type(search) == str and search.split(" ")[0] in self.allBuildings:
                if currentRoom != search:
                    roomFile.write(f'"{currentRoom}"' + ': ' + str(tempList).replace("'", '"') + ',\n')
                    currentRoom = search
                    tempList = []
    
            elif type(search) == str and search[0].isdigit():
                toAdd = loadedData.loc[row, 'Times'].split(', ')
                if len(toAdd) > 1:
                    toAdd = toAdd[1].split(' ')[:-2]
                    ' '.join(toAdd)
                    tempList.append(toAdd)
                else:
                    tempList.append('')
                    
        roomFile.write(f'"{currentRoom}"' + ': ' + str(tempList).replace("'", '"') + '\n}')
        
        
        roomDict = json.load(roomFile)
        
        roomFile.close()
        
        return roomDict
        
        
    def check_availability(self, roomList):
        now = datetime.now()
        nowDelta = timedelta(hours=now.hour, minutes=now.minute)
        dayOfWeek = now.strftime('%A')
        
        if dayOfWeek == 'Thursday':
            dayOfWeek = 'R'
        else:
            dayOfWeek = dayOfWeek[0]
            
        for timeSlot in range(len(roomList)):
            data = roomList[timeSlot]
            if len(data) > 1 and dayOfWeek in data[0]:
                startTime = datetime.strptime(data[1][:4], '%H%M')
                startDelta = timedelta(hours=startTime.hour, minutes=startTime.minute)
                
                endTime = datetime.strptime(data[1][5:], '%H%M')
                endDelta = timedelta(hours=endTime.hour, minutes=endTime.minute)
                
                if startDelta <= nowDelta < endDelta:
                    return f'UNAVAILABLE until {str(endTime.time())[:-3]}'
                 
                elif (nowDelta < startDelta):
                    return f'AVAILABLE   until {str(startDelta)[:-3]}'
    
        return 'AVAILABLE   rest of day'


ABS_PATH = __file__.removesuffix('checkerBoard.py')
root = tk.Tk()
root.title('UWIT Checkerboard')
root.geometry('750x630')
root.option_add('*Font', 'courier 12')
root.config(bg='#cbcccd')
root.update_idletasks()
checkerBoard = CheckerBoard(root)

def onResize(event):
    root.config(height=event.height, width=event.width)
    checkerBoard.set_list_size(root.winfo_height(), root.winfo_height())
    
root.bind('<Configure>', onResize)
root.bind('<Button-1>', checkerBoard.highlight_boxes)
root.bind('<Button-3>', checkerBoard.show_full_schedule)

checkerBoard.mainloop()
