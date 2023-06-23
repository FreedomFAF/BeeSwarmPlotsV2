from tkinter.filedialog import askopenfilename
from SelectorPages.BasePage import BasePage

import tkinter as tk

def checkFileType(fileChosen):
    dotLocation = fileChosen.index(".")
    fileExtension = ""
    if dotLocation != -1:
        fileExtension = fileChosen[dotLocation:]
    if fileExtension == ".csv":
        return True
    else:
        return False


class ImportPage(BasePage):
    pageName = "import"
    def __init__(self, master):
        super(ImportPage, self).__init__(master)

        typeHeaderLabel = tk.Label(self, text="Import")
        typeHeaderLabel.grid(row=2, column=0, sticky=tk.W, pady=6)

        self.fileChosen = None
        self.fileTypeOK = tk.StringVar()
        self.fileTypeOK.set("")

        self.importHold = tk.StringVar()
        self.importHold.set("")

        self.importHeaderMissing = tk.StringVar()
        self.importHeaderMissing.set("")

        self.isFileTypeOk = False

        selectFileButton = tk.Button(self, text='Select File', command=self.chooseFile).grid(row=3, column=0, sticky=tk.W, pady=6)

        self.fileTypeOKLabel = tk.Label(self, textvariable=self.fileTypeOK)
        self.fileTypeOKLabel.grid(row=3, column=2, sticky=tk.W, pady=6)

        selectFileHeader = tk.Label(self, text="File Selected")
        selectFileHeader.grid(row=4, column=0, sticky=tk.W, pady=6)

        self.selectFileLabel = tk.Label(self, textvariable=self.fileChosenText)
        self.selectFileLabel.grid(row=4, column=2, sticky=tk.W, pady=6)

        self.importHeaderMissingLabel = tk.Label(self, textvariable=self.importHeaderMissing)
        self.importHeaderMissingLabel.grid(row=6, column=0, sticky=tk.W, pady=6)

        self.importHoldLabel = tk.Label(self, textvariable=self.importHold)
        self.importHoldLabel.grid(row=6, column=2, sticky=tk.W, pady=6)

        goButton = tk.Button(self, text='Select Data', command=self.goToSelectData)
        goButton.grid(row=7, column=2, sticky=tk.W, pady=6)

    def chooseFile(self):
        fileChosen = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.dataStore.fileName = fileChosen
        self.fileChosenText.set(fileChosen)
        self.isFileTypeOk = checkFileType(fileChosen)
        if self.isFileTypeOk:
            self.fileTypeOK.set("")
        else:
            self.fileTypeOK.set("File must be a csv.")

    def goToSelectData(self):
        self.dataStore.loadData()
        self.master.switchFrame(self.master.frames["dataSelector"])


