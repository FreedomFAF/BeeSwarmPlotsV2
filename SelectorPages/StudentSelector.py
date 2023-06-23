from SelectorPages.BasePage import BasePage
from GraphUI.Screen import Screen

import tkinter as tk

class StudentSelectorPage(BasePage):
    pageName = "studentSelector"

    def __init__(self, master):
        super(StudentSelectorPage, self).__init__(master)

        pageLabel = tk.Label(self,text="Select Students")
        pageLabel.grid(row=0, column=0, sticky=tk.W, pady=6)

        currentRow = 1

        studentHeaderLabel = tk.Label(self, text="students in data")
        studentHeaderLabel.grid(row=currentRow, column=1, sticky=tk.W, pady=6)

        studentIncludeLabel = tk.Label(self, text="include")
        studentIncludeLabel.grid(row=currentRow, column=2, sticky=tk.W, pady=6)
        currentRow += 1

        self.studentsToInclude = {}
        students = self.dataStore.data[self.dataStore.studentColumn]
        for index, student  in students.items():
            studentNameLabel = tk.Label(self, text=student)
            studentNameLabel.grid(row=currentRow, column=1, sticky=tk.W, pady=6)

            self.studentsToInclude[index] = tk.IntVar()
            self.studentsToInclude[index].set(1)
            studentIncludeCheck = tk.Checkbutton(self, variable=self.studentsToInclude[index])
            studentIncludeCheck.grid(row=currentRow, column=2, sticky=tk.W, pady=6)
            currentRow += 1
        currentRow += 1

        goButton = tk.Button(self, text='Previous', command=self.goToDataSelector)
        goButton.grid(row=currentRow, column=0, sticky=tk.W, pady=6)

        goButton = tk.Button(self, text='Generate Graphs', command=self.generateGraphs)
        goButton.grid(row=currentRow, column=2, sticky=tk.W, pady=6)

    def goToDataSelector(self):
        self.master.switchFrame(self.master.frames["dataSelector"])


    def generateGraphs(self):
        studentsToUse = []
        for k, v in self.studentsToInclude.items():
            if v.get() == 1:
                studentsToUse.append(k)
        self.dataStore.selectedStudents = studentsToUse

        self.dataStore.getFinalData()

        Screen()