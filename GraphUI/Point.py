import pygame
from GraphUI.Colour import Colour

class Point(object):
    def __init__(self, student, chartName, score, location, size, colour=Colour.red):
        self.chartName = chartName
        self.colour = colour
        self.student = student
        self.score = score
        self.location = location
        self.size = size

        self.isSelected = False
        self.isHovered = False

    def draw(self, surface):
        if self.isSelected:
            pygame.draw.circle(surface, Colour.green.value, self.location, self.size + 2)
        elif self.isHovered:
            pygame.draw.circle(surface, Colour.blue.value, self.location, self.size + 2)
        else:
            pygame.draw.circle(surface, Colour.white.value, self.location, self.size + 2)
            pygame.draw.circle(surface, self.colour.value, self.location, self.size)

        self.isHovered = False

    def isOver(self, mouseLocation, chartLocation):
        mx, my = mouseLocation
        lx, ly = self.location
        clx, cly = chartLocation
        dx = abs(mx - (lx + clx))
        dy = abs(my - (ly + cly))
        R = self.size
        if dx > R:
            return False

        if dy > R:
            return False

        if dx + dy <= R:
            return True

        if dx ^ 2 + dy ^ 2 <= R ^ 2:
            return True

        else:
            return False

