from enum import Enum

class Colour(Enum):
    blue = (0, 0, 255)
    green = (0 , 255, 0)
    white = (255, 255, 255)
    black = (1, 0, 0)
    red = (255, 0, 0)
    cyan = (0, 255, 255)
    green_orange = (0, 255, 128)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    teal = (0, 128, 128)
    olive = (128, 128, 0)
    magenta = (255, 0, 255)
    light_blue = (0, 128, 255)
    grey = (128, 128, 128)
    orange = (255, 128, 0)
    indigo = (128,0,255)
    chartreuse = (128,255,0)
    pink = (255,0,128)

    @staticmethod
    def get(index):
        nameList = [member.name for member in Colour]
        return Colour[nameList[index]]
