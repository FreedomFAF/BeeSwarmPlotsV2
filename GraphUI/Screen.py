import pygame
import math
import os
from fpdf import FPDF

from DataStore import DataStore
from GraphUI.Chart import Chart
from GraphUI.Colour import Colour

def findSquare(num):
    root = math.sqrt(num)
    bigger = math.ceil(root)
    smaller = math.floor(root)
    if bigger*smaller < num:
        smaller += 1
    return [bigger, smaller]


class Screen(object):

    LEFT = 1
    RIGHT = 3

    def __init__(self):
        self.dataStore = DataStore.shared()
        pygame.init()
        infoObject = pygame.display.Info()
        self.clock = pygame.time.Clock()
        # sets the screen size
        self.screenSize = self.width, self.height = infoObject.current_w, infoObject.current_h
        # sets the screen to full screen
        self.screen = pygame.display.set_mode(self.screenSize, pygame.FULLSCREEN)
        self.screen.fill(Colour.white.value)
        pygame.display.set_caption('Results plotter')

        pygame.font.init()

        # do a count on the number of tests and then work out the size of each chart based on the size of the screen
        numberOfCharts = len(self.dataStore.chartsNeeded)
        chartGridSize = findSquare(numberOfCharts)
        chartSize = [math.floor(self.width/chartGridSize[0]), math.floor(self.height/chartGridSize[1])]
        self.UI = {}
        chartCount = 0
        chartX = 0
        chartY = 0
        for chartName in self.dataStore.chartsNeeded:
            if chartX == chartGridSize[0]:
                chartY += 1
                chartX = 0

            chartLocation = [chartX*chartSize[0],chartY*chartSize[1]]
            chartColumns = [chartName, self.dataStore.studentColumn]
            if self.dataStore.classColumn != "":
                chartColumns.append(self.dataStore.classColumn)
            chartData = self.dataStore.finalData[chartColumns]
            chartMax = self.dataStore.outOfRow[chartName]
            self.UI[chartName] = Chart(chartName, chartData, chartMax, chartSize, chartLocation)
            chartX += 1

        self.studentSelected = None
        self.getScreenShots = False
        self.screenShotCount = 0
        self.root = os.getcwd()
        self.screenShotFolder = os.path.join(self.root, 'ScreenShots')
        self.studentNames = self.dataStore.finalData[self.dataStore.studentColumn]
        self.pdf = FPDF(orientation='landscape', unit='pt', format=[self.height*1.1, self.width*1.1])
        self.mainLoop()


    def mainLoop(self):
        loopIt = True
        while loopIt:
            self.clock.tick(60)
            mousePosition = pygame.mouse.get_pos()

            for event in pygame.event.get():  # game code that happens when any button is pressed
                if event.type == pygame.QUIT:
                    loopIt = False
                     # closes the game in an event loop

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT:
                    self.studentSelected = None
                    for name, element in self.UI.items():
                        element.deselect()
                        if self.studentSelected == None:
                            self.studentSelected = element.isOver(mousePosition)

                elif event.type ==  pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT:
                    # right click
                    pass
                elif event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_ESCAPE:
                    # change this so that it opens the game menu
                    loopIt = False

                elif event.type ==  pygame.KEYDOWN and event.key ==  pygame.K_s:
                    # the d key is pressed
                    self.initiateScreenShotGenerator()

            studentHovered = None
            for name, element in self.UI.items():
                if studentHovered == None:
                    studentHovered = element.isOver(mousePosition)

            for name, element in self.UI.items():
                if self.studentSelected != None:
                    element.selectHighLightStudent(self.studentSelected)

                if studentHovered != None and studentHovered != self.studentSelected:
                    element.hoverHighLightStudent(studentHovered)
                element.draw(self.screen)
                element.removeLegend()

            self.getScreenShot()
            pygame.display.update()
        pygame.display.quit()


    def initiateScreenShotGenerator(self):
        self.getScreenShots = True
        if not os.path.isdir(self.screenShotFolder):
            os.mkdir(self.screenShotFolder)
        os.chdir(self.screenShotFolder)

    def getScreenShot(self):
        if self.getScreenShots:
            for name, element in self.UI.items():
                element.deselect()

            if self.screenShotCount > 0:
                spriteName = os.path.join(self.screenShotFolder, self.studentNames.loc[self.screenShotCount] + ".png")
                pygame.image.save(self.screen, spriteName)
                self.pdf.add_page()
                self.pdf.image(spriteName)
            else:
                spriteName = os.path.join(self.screenShotFolder, "TeacherVersion.png")
                pygame.image.save(self.screen, spriteName)
                self.pdf.add_page()
                self.pdf.image(spriteName)

            self.screenShotCount += 1

            if self.screenShotCount == len(self.dataStore.selectedStudents) + 1:
                self.getScreenShots = False
                self.screenShotCount = 0
                self.studentSelected = None
                self.pdf.output(name='ScreenShotsToPrint.pdf',dest='F')

            else:
                self.studentSelected = self.studentNames.loc[self.screenShotCount]





