import pandas as pd
import os
import json
import logging
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
                available = self.check_availability(self.load_zones[room])
                string = f'{room:11} | {available}'
                roomList.append(string)
        return roomList

    
    def pull_zones(self):
        roomsDict = {}
        
        if os.path.exists(self.ABS_PATH + 'rooms.json'):
            config = open(self.ABS_PATH + 'rooms.json', 'r')
            roomsDict = json.load(config)
            
        else:
            roomsDict = self.generate_config()
    
        return roomsDict
    

    def generate_config(self):
        
        ABS_PATH = __file__.removesuffix('zoneConfig.py')
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
                
                if startDelta <= nowDelta <= endDelta:
                    return f'UNAVAILABLE until {endTime.time()}'
                
                elif (timeSlot < len(roomList)-1):
                    nextData = roomList[timeSlot+1]
                    if len(nextData) > 1 and dayOfWeek in nextData[0]:
                        nextTime = datetime.strptime(nextData[1][:4], '%H%M')
                        nextDelta = timedelta(hours=nextTime.hour, minutes=nextTime.minute)
                    
                        if (nowDelta < nextDelta):
                            return f'AVAILABLE   until {str(nextDelta)}'
                        
    
        return 'AVAILABLE'