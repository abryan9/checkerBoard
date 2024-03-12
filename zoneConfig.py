import pandas as pd
import os

class zone_config():

    def __init__(self):
        self.load_zones = self.generate_config()
        
        self.ABS_PATH = __file__.removesuffix('zoneConfig.py')


    def get_zone(self, zoneNum):
        zoneList = [
            [['AG', 0], ['EERB', 0], ['STEM', 0], ['SI', 0], ['GE', 0], ['PS', 0], ['BS', 0], ['AB', 0], ['AC', 0], ['AS', 0], ['CR', 0], ['CL', 0], ['BU', 0], ['ITC', 0], ['PA', 0], ['LS', 0], ['VA', 0], ['CB', 0], ['HA', 0], ['ED', 0], ['EA', 0], ['ESB', 0], ['EIC', 0], ['HS', 0], ['NA', 0], ['HI', 0],],
            ['AG'],
            ['EN'],
            ['CR'],
            ['LS'],
            [],
        ]
        
        return zoneList[zoneNum]

    
    def pull_zones(self):
        if os.path.isFile(self.ABS_PATH + 'zone.config'):
            config = open(self.ABS_PATH + 'zone.config', 'r')
            for line in config:
                print(line)
                
            config.close()
        
        return 0
    

    def generate_config(self):
        roomList = [
            'SI', 'STEM', 'EERB', 'AN', 'BC', 'HS', 'GE', 'ES', 'EIC',
            'EN', 'AG', 'EA', 'ED', 'HA', 'HI', 'BU',
            'CR', 'PS', 'AS', 'BS', 'NAC', 'RH', 'HO',
            'PA', 'FA', 'CB', 'LS', 'AB', 'AC', 'VA',
        ]
        
        ABS_PATH = __file__.removesuffix('zoneConfig.py')
        data = (ABS_PATH + 'roomConfig.csv')
        loadedData = pd.read_csv(data, names=['Rooms', 'Times', 'Contact', 'Empty'], engine='pyarrow', header=None)
        
        rows, columns = loadedData.shape
        
        roomDict = {}
        currentRoom = ''
        tempList = []
        for row in range(rows):
            search = loadedData.loc[row, 'Rooms']
            if type(search) == str and search.split(" ")[0] in roomList:
                if currentRoom != search:
                    if currentRoom != '':
                        roomDict.update({search: tempList})
                    currentRoom = search
                    tempList = []
            
            elif type(search) == str and search[0].isdigit():
                tempList.append(search)
                
            
        
        print(roomDict)
        
        return roomDict