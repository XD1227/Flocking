import math
import Vector
import Vehicle

class Grids(object):
    def __init__(self, width, height, r):
        self.resolution = r
        self.cols = int(width / r)
        self.rows = int(height / r)
        self.grids = [[[] for col in range(self.cols)] for row in range(self.rows)]
    
    def init(self, vehicles):
        self.grids = [[[] for col in range(self.cols)] for row in range(self.rows)]

        for vehicle in vehicles:
            column = int(self.constrain(vehicle.location.x / self.resolution, 0, self.cols-1))
            row = int(self.constrain(vehicle.location.y / self.resolution, 0, self.rows-1))
            self.grids[row][column].append(vehicle.id)
    def getneighbors_onlyfromonecell(self, pos):
        vehiclesids = []
        column = int(self.constrain(pos.x / self.resolution, 0, self.cols-1))
        row = int(self.constrain(pos.y / self.resolution, 0, self.rows-1))
        grid = self.grids[row][column]
        index = 0
        for id in grid:
            vehiclesids.append(id) 
            index += 1
            if index > 10: break      
        return vehiclesids

    def getneighbors(self, pos):
        column = int(self.constrain(pos.x / self.resolution, 0, self.cols-1))
        row = int(self.constrain(pos.y / self.resolution, 0, self.rows-1))
        Neighbors = []
        Neighbors.append([row, column])
        # x - axis
        if pos.x % self.resolution < self.resolution / 2:
            Neighbors.append([row, self.wrap(column - 1, 0, self.cols - 1)])
        else:
            Neighbors.append([row, self.wrap(column + 1, 0, self.cols - 1)])
        # y - axis
        if pos.y % self.resolution < self.resolution / 2:
            Neighbors.append([self.wrap(row - 1, 0, self.rows - 1), column])
            Neighbors.append([self.wrap(row - 1, 0, self.rows - 1), Neighbors[1][1]])
        else:
            Neighbors.append([self.wrap(row + 1, 0, self.rows - 1), column])
            Neighbors.append([self.wrap(row + 1, 0, self.rows - 1), Neighbors[1][1]])
        vehiclesids = []
        index = 0
        for neighbor in Neighbors:
            r = neighbor[0]
            c = neighbor[1]
            if r < 0 or c < 0: continue 
            grid = self.grids[r][c]
            for id in grid:
                index += 1
                if index > 10: break     
                vehiclesids.append(id)
        
        return vehiclesids
    def wrap(self, x, lo, hi):
        if x < lo: return x + (hi - lo)
        elif x > hi: return x - (hi - lo)
        else: return x
    def constrain(self, a, min_, max_):
        if math.isnan(a): 
            return 0
        if a < min_: a = min_
        elif a > max_: a = max_
        return a