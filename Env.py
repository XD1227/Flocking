import time
import sys
import tkinter as tk
import Vector
from Vehicle import *
# from FlowField import *
from Path import *
from SpatialSubdivison import Grids

class Env(tk.Tk, object):
    def __init__(self, vehicles, flow=None, path=None):
        super(Env, self).__init__()
        self.vehicles = vehicles
        self.vehicles_array = []  
        self.flow = flow
        self.path = path
        self.target = PVector(600., 200.)
        self.title('Flocking')
        self.geometry('{0}x{1}'.format(ENV_W, ENV_H))
        self.init()

    def processMouseEvent(self, event):
        oldpos = copy.deepcopy(self.target) 
        self.target = PVector(event.x, event.y)
        changed = PVector.sub_s(self.target, oldpos)
        # self.canvas.move(self.rect, changed.x, changed.y)

    def init(self):
        self.grids = Grids(ENV_W, ENV_H, 20)
        self.grids.init(self.vehicles
        self._build_env()
    def _build_env(self):
        # 所有部件都是在canvas(画布)上面画的
        self.canvas = tk.Canvas(self, bg='white', height= ENV_H, width=ENV_W)
        self.canvas.pack() # 挂载
        # draw vehicles
        for vehicle in self.vehicles:
            points = vehicle.coords()
            tri = self.canvas.create_polygon(points, outline='red', fill='green')           
            self.vehicles_array.append(tri)
            
        if self.flow is not None:            
            # draw flowline
            flow_lines = self.flow.coords_lines()
            for line in flow_lines:
                self.canvas.create_line(line[0].x, line[0].y, line[1].x, line[1].y, width=1, arrow=tk.LAST, fill='black')
        if self.path is not None:
            points = []
            for point in self.path.points:
                points.append(point.x)
                points.append(point.y)
            self.canvas.create_line(points, width=20, fill='black')
        self.canvas.bind(sequence="<Button-1>", func=self.processMouseEvent)
 
    def step(self):
        for vehicle in self.vehicles_array:
            self.canvas.delete(vehicle)
        self.vehicles_array.clear() 

        for i in range(len(self.vehicles)):
            vehicle = self.vehicles[i]
            neighborids = self.grids.getneighbors(vehicle.location)
            neighbors = []
            for id in neighborids:
                neighbors.append(self.vehicles[id])
            # vehicle.followflow(self.flow)
            # vehicle.followpath(self.path)
            vehicle.flocking(neighbors)
            vehicle.update()        
        for vehicle in self.vehicles:
            points = vehicle.coords()
            tri = self.canvas.create_polygon(points, outline='red', fill='green')
            self.vehicles_array.append(tri)
        self.grids.init(self.vehicles)
        self.update()

def generaterandom(min_, max_):
    return min_ + np.random.rand() * (max_ - min_) 


def update():
    while True:
        env.step()
        time.sleep(0.05)

def newpath():
    path = Path()
    path.addpoint(-20, ENV_H / 2)
    path.addpoint(generaterandom(0, ENV_W / 2), generaterandom(0, ENV_H))
    path.addpoint(generaterandom(ENV_W / 2, ENV_W), generaterandom(0, ENV_H))
    path.addpoint(ENV_W + 20, ENV_H / 2)
    return path

if __name__ == '__main__':
    # # flow field
    # flowfield = FlowField(ENV_W, ENV_H, 30)
    # # path
    # path = newpath()

    vehicles = []
    for i in range(300):
        vehicles.append(Vehicle(i, generaterandom(0,ENV_W), generaterandom(0,ENV_H)))

    env = Env(vehicles) # 实例化Env
    env.after(100, update)
    env.mainloop()  #显示
