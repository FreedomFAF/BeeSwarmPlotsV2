import pandas as pd
import copy

class DataStore(object):
    instance = False

    @staticmethod
    def shared():
        if not DataStore.instance:
            DataStore.instance = DataStore()
        return DataStore.instance

    def __init__(self):
        self.fileName = ""
        self.data = None
        self.outOfRow = None
        self.finalData = None

        self.studentColumn = ""
        self.chartsNeeded = []

        self.selectedColumns = []
        self.selectedStudents = []


    def loadData(self):
        self.data = pd.read_csv(self.fileName)
        self.outOfRow = self.data.iloc[0]
        self.data.drop(index=0, inplace=True)

    def getStudents(self):
        return self.data["student"]

    def getFinalData(self):
        self.finalData = self.data.loc[self.selectedStudents, self.selectedColumns]
        self.chartsNeeded = copy.deepcopy(self.selectedColumns)
        self.chartsNeeded.remove(self.studentColumn)