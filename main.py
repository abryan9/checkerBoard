import tkinter as tk
from tkinter import ttk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.everythingy = tk.Entry()
        self.everythingy.pack()
        
        self.contents = tk.StringVar()
        self.contents.set("This is a variable")
        # self.contents.append("This is another variable")
        self.everythingy["textvariable"] = self.contents
        
        self.everythingy.bind('<Key-Return>', self.print_contents)
    
    def print_contents(self, event):
        print("The current entries are:",
                self.contents.get())
    

root = tk.Tk()
myapp = App(root)
frm = ttk.Frame(myapp, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
myapp.mainloop()
