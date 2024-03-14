import pandas as pd
import os
from datetime import date, datetime, timedelta
import calendar

class zone_config():

    ABS_PATH = __file__.removesuffix('zoneConfig.py')
    
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
        
        roomList = []
        for room in self.load_zones.keys():
            if room.split(" ")[0] in zoneList[zoneNum]:
                roomList.append([room, self.load_zones[room]])
                self.check_availability(self.load_zones[room])

        return roomList

    
    def pull_zones(self):
        roomsDict = {}
        
        if os.path.exists(self.ABS_PATH + 'rooms.conf'):
            config = open(self.ABS_PATH + 'rooms.conf', 'r')
            for line in config:
                splitList = line[:-2].split(': ')
                roomsDict.update({str(splitList[0]): str(splitList[1][1:])[1:-2].split('], [')})
                
            config.close()
            
        else:
            roomsDict = self.generate_config()
    
        return roomsDict
    

    def generate_config(self):
        
        ABS_PATH = __file__.removesuffix('zoneConfig.py')
        data = (ABS_PATH + 'roomConfig.csv')
        loadedData = pd.read_csv(data, names=['Rooms', 'Times', 'Contact', 'Empty'], engine='pyarrow', header=None)
        roomFile = open(ABS_PATH + 'rooms.conf', 'w')
        
        rows, columns = loadedData.shape
        
        roomDict = {}
        currentRoom = 'AB 103'
        tempList = []
        for row in range(rows):
            search = loadedData.loc[row, 'Rooms']
            if type(search) == str and search.split(" ")[0] in self.allBuildings:
                if currentRoom != search:
                    roomDict.update({currentRoom: tempList})
                    roomFile.write(currentRoom + ': ' + str(tempList) + '\n')
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
                    
        roomDict.update({currentRoom: tempList})
        roomFile.write(currentRoom + ': ' + str(tempList) + '\n')
        
        roomFile.close()
        
        return roomDict
        
        
    def check_availability(self, roomList):
        now = datetime.now()
        dayOfWeek = now.strftime('%A')
        
        if dayOfWeek == 'Thursday':
            dayOfWeek = 'R'
        else:
            dayOfWeek = dayOfWeek[0]
            
        for room in roomList:
            print(room)