from Vector import *
from noise import pnoise2
import math

class FlowField(object):
    def __init__(self, width, height, r):
        self.resolution = r
        self.cols = int(width / r)
        self.rows = int(height / r)
        self.field = [[None for col in range(self.cols)] for row in range(self.rows)]
        self.init()

    def init(self):
        xoff = 0
        for i in range(self.rows):
            yoff = 0
            for j in range(self.cols):
                theta = pnoise2(xoff, yoff) * math.pi * 2
                self.field[i][j] = PVector(math.cos(theta), math.sin(theta))
                yoff += 0.05
            xoff += 0.1
    
    def lookup(self, lookup_):
        def constrain(a, min_, max_):
            if math.isnan(a): 
                return 0
            if a < min_: a = min_
            elif a > max_: a = max_
            return a
        column = int(constrain(lookup_.x / self.resolution, 0, self.cols-1))
        row = int(constrain(lookup_.y / self.resolution, 0, self.rows-1))
        return self.field[row][column]
    
    # 在每个field中画点
    def coords(self):
        points = []
        for i in range(self.rows):
            for j in range(self.cols):
                # midddle point
                y = (i + 0.5) * self.resolution
                x = (j + 0.5) * self.resolution
                points.append(PVector(x, y))
        return points
    def coords_lines(self):
        lines = []
        for i in range(self.rows):
            for j in range(self.cols):
                vector = self.field[i][j]
                heading = math.atan2(vector.y, vector.x) - math.pi / 2
                cos_val = math.cos(heading)
                sin_val = math.sin(heading)

                # midddle point
                y = (i + 0.5) * self.resolution
                x = (j + 0.5) * self.resolution

                line = []
                points = [[0, -5], [0, 5]]
                for x_old, y_old in points:
                    x_new = x_old * cos_val - y_old * sin_val
                    y_new = x_old * sin_val + y_old * cos_val
                    x_new += x
                    y_new += y
                    line.append(PVector(x_new, y_new))

                lines.append(line)
        return lines