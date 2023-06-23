import tkinter as tk
from SelectorPages.ImportPage import ImportPage
from SelectorPages.DataSelectorPage import DataSelectorPage
from SelectorPages.StudentSelector import StudentSelectorPage
from DataStore import DataStore

class TkApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.data = DataStore.shared()

        self.frames = {"import":ImportPage,
                       "dataSelector":DataSelectorPage,
                       "studentSelector":StudentSelectorPage}

        self.geometry("1200x1200")
        self.frame = None

        self.switchFrame(ImportPage)

    def switchFrame(self, frameClass):
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.frame.grid(row=0, column=0, sticky="nsew")

