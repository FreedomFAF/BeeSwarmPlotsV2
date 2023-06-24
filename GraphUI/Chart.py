from DataStore import DataStore
from GraphUI.Point import Point
from GraphUI.Colour import Colour

import pygame
import math
import copy

class Chart(object):
    def __init__(self, chartName, dataList, maxScore, size, location):
        # the input variables
        self.maxScore = maxScore
        self.size = size
        self.location = location
        self.chartName = chartName
        self.dataList = dataList

        # relative chart locations
        self.middleX = math.floor(self.size[0]*0.5)
        self.leftX = math.floor(self.size[0] * 0.05)
        self.rightX = math.floor(self.size[0] * 0.95)

        self.bottomY = math.floor(self.size[1] * 0.90)
        self.topY = math.floor(self.size[1] * 0.1)

        stepSize = math.ceil((self.topY - self.bottomY) / self.maxScore)
        self.hundredPercentY = stepSize * self.maxScore

        self.pointSize = 5
        self.pointSpacing = 1

        self.axisWidth = 1

        self.points = {}
        self.dataStore = DataStore.shared()
        self.image = pygame.Surface(size)
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.scores = [[] for _ in range(self.maxScore + 1)]

        self.myFont = pygame.font.SysFont('arial', 16)
        self.myAxisFont = pygame.font.SysFont('arial', 12)

        self.myTitleFont = pygame.font.SysFont('arial', 18)
        self.myTitleFont.set_bold(True)
        self.myTitleFont.set_underline(True)
        self.myLegendFont = pygame.font.SysFont('arial', 16)
        self.myLegendFont.set_underline(True)

        #Draw axis
        self.drawAxis()
        # print the title to the graph
        fontSpaceMiddle = [math.floor(self.size[0] * 0.5), math.floor(self.size[1] * 0.05)]
        titleImage = self.myTitleFont.render(chartName, False, Colour.black.value)
        titleSize = self.myTitleFont.size(chartName)
        titleLocation = [fontSpaceMiddle[0] - math.floor(titleSize[0]/2), fontSpaceMiddle[1] - math.floor(titleSize[1]/2)]
        self.image.blit(titleImage, titleLocation)

        #print Legend
        self.legendX = math.floor(self.size[0] * 0.05)
        self.legendY = math.floor(self.size[1] * 0.1)
        legendImage = self.myLegendFont.render('Legend:', False, Colour.black.value)
        self.image.blit(legendImage, (self.legendX, self.legendY))
        self.legendY += self.myLegendFont.size('Legend:')[1]
        self.legendDefaultY = copy.deepcopy(self.legendY)
        self.legendXMax = self.legendX

        coloursAssigned = {}
        startColourNumber = 4

        for a in range(len(dataList)):
            dataRow = dataList.iloc[a]
            score = dataRow[chartName]
            xPos =  int(self.pointXPos(len(self.scores[score])) * ((self.pointSize + self.pointSpacing) * 2) + self.middleX)
            yPos = self.bottomY + score*stepSize
            location = [xPos, yPos]

            student = dataRow[self.dataStore.studentColumn]
            if self.dataStore.classColumn != "":
                studentsClass = dataRow[self.dataStore.classColumn]
                if studentsClass in coloursAssigned.keys():
                    studentsColour = coloursAssigned.get(studentsClass)
                else:
                    studentsColour = Colour.get(startColourNumber)
                    coloursAssigned[studentsClass] = studentsColour
                    startColourNumber += 1
                newPoint = Point(student, chartName, score, location, self.pointSize, studentsColour)
            else:
                newPoint = Point(student, chartName, score, location, self.pointSize)
            self.points[student] = newPoint
            self.scores[score].append(newPoint)

        for score in self.scores:
            half = len(score)/2
            if half == math.floor(half):
                for point in score:
                    point.location[0] += self.pointSize + self.pointSpacing



    def pointXPos(self,number):
        half = number/2
        if half == math.floor(half):
            return half
        else:
            return -math.ceil(half)

    def drawAxis(self):
        pygame.draw.line(self.image,
                         Colour.black.value,
                         [self.leftX, self.bottomY],
                         [self.rightX, self.bottomY],
                         self.axisWidth)
        pygame.draw.line(self.image,
                         Colour.black.value,
                         [self.middleX, self.bottomY],
                         [self.middleX, self.topY],
                         self.axisWidth)

        percentages = [25,50,75,100]
        for percentage in percentages:
            percentageText = self.myAxisFont.render(str(percentage) +'%', False, Colour.black.value)
            xLocation = self.middleX - math.floor(percentageText.get_width()*1.25)
            yLocation = math.floor(self.hundredPercentY * percentage / 100) + self.bottomY - math.floor(percentageText.get_height()/2)
            self.image.blit(percentageText, [xLocation,yLocation])

    def draw(self, screen):
        for student, point in self.points.items():
            point.draw(self.image)
        screen.blit(self.image, self.location)

    def isOver(self, mousePosition):
        mx, my = mousePosition
        lx, ly = self.location
        sx, sy = self.size
        if lx <= mx < sx + lx and  ly <= my < sy + ly:
            for student, point in self.points.items():
                if point.isOver(mousePosition, self.location):
                    return student

        return None

    def deselect(self):
        for student, point in self.points.items():
            point.isSelected = False

    def selectHighLightStudent(self, student):
        self.points[student].isSelected = True

        legendText = student + ': ' + str(self.points[student].score)
        selectLegendText = self.myFont.render(legendText, False, Colour.black.value)

        self.image.blit(selectLegendText, (self.legendX, self.legendY))


        pointLocation = [self.legendX + selectLegendText.get_width() + self.pointSpacing + 2*self.pointSize, self.legendY + math.floor(selectLegendText.get_height()/2)]

        selectLegendPoint = Point('legendSelect', self.chartName, 0, pointLocation, self.pointSize)
        selectLegendPoint.isSelected = True
        selectLegendPoint.draw(self.image)

        self.legendY += selectLegendText.get_height()

        xMax = self.legendX + selectLegendText.get_width() + (self.pointSize * 2) + (self.pointSpacing * 2)
        if xMax > self.legendXMax:
            self.legendXMax = xMax

    def hoverHighLightStudent(self, student):
        self.points[student].isHovered = True

        legendText = student + ': ' + str(self.points[student].score)
        hoverLegendText = self.myFont.render(legendText, False, Colour.black.value)

        self.image.blit(hoverLegendText, (self.legendX, self.legendY))
        pointLocation = [self.legendX + hoverLegendText.get_width() + self.pointSpacing + 2*self.pointSize, self.legendY + math.floor(hoverLegendText.get_height()/2)]

        hoverLegendPoint = Point('legendSelect', self.chartName, 0, pointLocation, self.pointSize)
        hoverLegendPoint.isHovered = True
        hoverLegendPoint.draw(self.image)
        self.legendY += hoverLegendText.get_height()

        xMax = self.legendX + hoverLegendText.get_width() + (self.pointSize * 2) + (self.pointSpacing * 2)
        if xMax > self.legendXMax:
            self.legendXMax = xMax

    def removeLegend(self):
        rectangle = pygame.Rect(self.legendX,self.legendDefaultY, self.legendXMax, self.legendY)
        pygame.draw.rect(self.image, Colour.white.value, rectangle)
        self.legendY = self.legendDefaultY
        self.legendXMax = self.legendX
