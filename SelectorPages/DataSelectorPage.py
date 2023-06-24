from SelectorPages.BasePage import BasePage

import tkinter as tk

class DataSelectorPage(BasePage):
    pageName = "dataSelector"
    def __init__(self, master):
        super(DataSelectorPage, self).__init__(master)

        typeHeaderLabel = tk.Label(self, text="Select Columns")
        typeHeaderLabel.grid(row=0, column=0, sticky=tk.W, pady=6)

        currentRow = 1
        currentColumn = 1

        headerLabel = tk.Label(self, text="header")
        headerLabel.grid(row=1, column=0, sticky=tk.W, pady=6)
        headerCheckboxLabel = tk.Label(self, text="Include")
        headerCheckboxLabel.grid(row=2, column=0, sticky=tk.W, pady=6)

        headerOptionMenu = {}
        self.headerIncludes = {}
        for column in self.dataStore.data.columns:
            headerLabel = tk.Label(self, text=column)
            headerLabel.grid(row=currentRow, column=currentColumn, sticky=tk.W, pady=6)

            self.headerIncludes[column] = tk.IntVar()
            self.headerIncludes[column].set(1)
            headerOptionMenu[column] = tk.Checkbutton(self,variable=self.headerIncludes[column])
            headerOptionMenu[column].grid(row=currentRow + 1, column=currentColumn, sticky=tk.W, pady=6)
            currentColumn += 1
        currentRow += 3

        ssLabel = tk.Label(self, text="Select the column of Student Names:")
        ssLabel.grid(row=currentRow, column=0, sticky=tk.W, pady=6)

        studentColumnChoices = self.dataStore.data.columns.tolist()
        studentColumnChoices.append("")
        studentColumnOptionMenu = tk.OptionMenu(self, self.studentColumn, *studentColumnChoices)
        studentColumnOptionMenu.grid(row=currentRow, column=1, sticky=tk.W, pady=6)
        currentRow += 1

        ssLabel = tk.Label(self, text="Select the Class column:")
        ssLabel.grid(row=currentRow, column=0, sticky=tk.W, pady=6)

        studentColumnOptionMenu = tk.OptionMenu(self, self.classColumn, *studentColumnChoices)
        studentColumnOptionMenu.grid(row=currentRow, column=1, sticky=tk.W, pady=6)
        currentRow += 1

        outOfRowWarning = tk.Label(self, text="Please note the first row will be used as the Maximum score for each question", wraplength=200)
        outOfRowWarning.grid(row=currentRow, column=0, sticky=tk.W, pady=6)
        currentRow += 1

        goButton = tk.Button(self, text='Previous', command=self.goToImportPage)
        goButton.grid(row=currentRow, column=0, sticky=tk.W, pady=6)

        goButton = tk.Button(self, text='Select Students', command=self.goToStudentSelector)
        goButton.grid(row=currentRow, column=2, sticky=tk.W, pady=6)

    def goToImportPage(self):
        self.master.switchFrame(self.master.frames["import"])

    def goToStudentSelector(self):
        self.dataStore.studentColumn = self.studentColumn.get()
        self.dataStore.classColumn = self.classColumn.get()
        columnsToUse = []
        for k, v in self.headerIncludes.items():
            if v.get() == 1:
                columnsToUse.append(k)
        self.dataStore.selectedColumns = columnsToUse
        self.master.switchFrame(self.master.frames["studentSelector"])