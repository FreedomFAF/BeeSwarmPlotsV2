import tkinter as tk
from DataStore import DataStore

class BasePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.dataStore = DataStore.shared()

        self.fileChosenText = tk.StringVar()
        self.fileChosenText.set(self.dataStore.fileName)

        self.studentColumn = tk.StringVar()
        self.studentColumn.set(self.dataStore.studentColumn)