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

        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.mainFrame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollBar = tk.Scrollbar(self.mainFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind(
            '<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.switchFrame(ImportPage)

    def switchFrame(self, frameClass):
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")
        #self.frame.grid(row=0, column=0, sticky="nsew")

