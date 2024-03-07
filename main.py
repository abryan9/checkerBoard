import tkinter as tk
from tkinter import ttk

class CheckerBoard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.label = tk.Label(self, text = " _|_ ")
        # self.label.pack()
        
        self.zones = ["No Zone Selected", "All Zones", "Zone 1", "Zone 2", "Zone 3", "Zone 4"]
        self.zone = tk.StringVar()
        
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
            "No Zone Selected": [], 
            "All Zones": ["1", "2", "3", "4"], 
            "Zone 1": ["1"],
            "Zone 2": ["2"],
            "Zone 3": ["3"],
            "Zone 4": ["4"],
        }
        
        print(zoneDict[zone])
        pass
    
    
    
    

root = tk.Tk()
root.title("CheckerBoard")
root.geometry("300x300")

checkerBoard = CheckerBoard(root)
frm = ttk.Frame(checkerBoard, padding=10)
frm.pack()

checkerBoard.select_zone()
# checkerBoard.show_rooms()

# ttk.Button(root, text="Quit", command=root.destroy).pack()
checkerBoard.mainloop()
