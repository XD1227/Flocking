import numpy as np 
import math

class PVector(object):
    def __init__(self, x = 0., y = 0.):
        self.x = x
        self.y = y
    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def add(self, x, y):
        self.x += x
        self.y += y
    def sub(self, x, y):
        self.x -= x
        self.y -= y
    def mult(self, v):
        if isinstance(v, (int, float)):
            self.x *= v
            self.y *= v
        else:
            self.x *= v.x 
            self.y *= v.y 
    def div(self, v):
        if isinstance(v, (int, float)):
            self.x /= v
            self.y /= v
        else:
            self.x /= v.x 
            self.y /= v.y 
    def setmag(self, n):
        self.normalize()
        self.mult(n)
    def dist(self, v):
        x = self.x - v.x
        y = self.y - v.y
        return math.sqrt(x * x + y * y)
    def dot(self, v):
        v1 = np.array([self.x, self.y])
        v2 = np.array([v.x, v.y])
        return np.dot(v1, v2)
    def cross(self, v):
        v1 = np.array([self.x, self.y])
        v2 = np.array([v.x, v.y])
        return np.cross(v1, v2)
    def normalize(self):
        m = self.mag()
        if m > 0: 
            self.div(m)
    def limit(self, high):
        if self.mag() > high:
            self.normalize()
            self.mult(high)
    def heading(self):
        return math.atan2(self.y, self.x)
    def __str__(self):
        return  "[" + self.x + ", " + self.y + "]"
    
    @staticmethod
    def add_s(v1, v2):
        return PVector(v1.x + v2.x, v1.y + v2.y)
    @staticmethod
    def sub_s(v1, v2):
        return PVector(v1.x - v2.x, v1.y - v2.y)
    @staticmethod
    def dist_s(v1, v2):
        v1 = np.array([v1.x, v1.y])
        v2 = np.array([v2.x, v2.y])
        return np.linalg.norm(v1 - v2) # 两点直接距离
    @staticmethod
    def dot_s(v1, v2):
        v1 = np.array([v1.x, v1.y])
        v2 = np.array([v2.x, v2.y])
        return np.dot(v1, v2)
    @staticmethod
    def cross_s(v1, v2):
        v1 = np.array([v1.x, v1.y])
        v2 = np.array([v2.x, v2.y])
        return np.cross(v1, v2)
    @staticmethod
    def angleBetween_s(v1, v2):
        v1 = np.array([v1.x, v1.y])
        v2 = np.array([v2.x, v2.y])

if __name__ == '__main__':
    v1 = PVector(0, 0)
    v2 = PVector(1, 1)
    v3 = v1 + v2

    
        
    
