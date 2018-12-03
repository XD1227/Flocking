from Vector import *

class Path(object):
    def __init__(self):
        self.radius = 20
        self.points = []
    def addpoint(self, x, y):
        self.points.append(PVector(x, y))
    def getstart(self):
        if len(self.points) > 0:
            return self.points[0]
        return None
    def getend(self):
        if len(self.points) > 0:
            return self.points[-1]
        return None
    