from Vector import PVector   # 自己编写的向量操作类
import math
import copy
import numpy as np 

ENV_H = 500  # grid height
ENV_W = 900  # grid width
PanicDistance = 100.0 
Radius = 1.5

class Vehicle(object):
    def __init__(self, id, x, y):
        self.id = id      # 车辆编号
        self.location = PVector(x, y)  # 位置
        self.velocity = PVector(0.5, 0.5)  # 速度
        self.acceleration = PVector(0, 0)  # 加速度
        self.maxspeed = 5   # 最大速度
        self.maxforce = 0.2  # 最大受力
        self.points = [[0, 6], [-3, -3], [3, -3]] # 三角形
        self.wandertheta = 0
        self.r = 3.0
        self.radius = 10
    
    def seek(self, target):
        desired = PVector.sub_s(target, self.location) # 获取预期速度方向 
        desired.normalize()  # 预期速度单位化
        desired.mult(self.maxspeed) # 乘以最大速度，即为最终预期速度
        steer = PVector.sub_s(desired, self.velocity)  # 预期速度 - 当前速度     
        steer.limit(self.maxforce) # 控制操纵力不能超过maxforce
        # self.applyForce(steer)  # 执行操作力
        return steer
    
    def arrive(self, target):
        desired = PVector.sub_s(target, self.location)
        d = desired.mag()
        desired.normalize()
        if d < PanicDistance:
            m = d * self.maxspeed / PanicDistance # map(d, 0, 100, 0, maxspeed)
            desired.mult(m)
        else:
            desired.mult(self.maxspeed)
        steer = PVector.sub_s(desired, self.velocity)
        steer.limit(self.maxforce)
        self.applyForce(steer)
    
    def wander(self):
        wanderR = Radius * 2
        wanderD = Radius * 10
        change = 0.3
        rand = -change + np.random.rand(1) * change * 2
        self.wandertheta += rand
        circleloc = copy.deepcopy(self.velocity) 
        circleloc.setmag(wanderD)
        circleloc.add(self.location.x, self.location.y)

        h = self.velocity.heading()
        wx = wanderR * math.cos(self.wandertheta + h)
        wy = wanderR * math.sin(self.wandertheta + h)
        circleOffset = PVector(wx, wy)
        target = PVector.add_s(circleloc, circleOffset)
        self.seek(target)

    def followflow(self, flow):
        if flow is None: return
        desired = flow.lookup(self.location)
        desired.normalize()
        desired.mult(self.maxspeed)
        steer = PVector.sub_s(desired, self.velocity)
        steer.limit(self.maxforce)
        self.applyForce(steer)
    
    def followpath(self, path):
        if path is None: return
        predict = copy.deepcopy(self.velocity)
        predict.normalize()
        predict.mult(50)
        predictpos = PVector.add_s(self.location, predict)

        normal = None
        target = None
        worldRecord = 1000000

        for i in range(len(path.points)-1):
            a = path.points[i]
            b = path.points[i+1]
            normalPoint = self.getNormalPoint(predictpos, a, b)
            if normalPoint.x < a.x or normalPoint.x > b.x:
                normalPoint = b
            distance = PVector.dist_s(predictpos, normalPoint)
            if distance < worldRecord:
                worldRecord = distance
                normal = normalPoint

                dir = PVector.sub_s(b, a)
                dir.normalize()
                dir.mult(10)
                target = copy.deepcopy(normalPoint)
                target.add(dir.x, dir.y)
        
        if worldRecord > path.radius:
            self.seek(target)

    def flocking(self, vehicles):
        sep = self.separate_flocking(vehicles)
        ali = self.align_flocking(vehicles)
        coh = self.cohesion_flocking(vehicles)

        sep.mult(3.5)
        ali.mult(1.0)
        coh.mult(1.0)

        self.applyForce(sep)
        self.applyForce(ali)
        self.applyForce(coh)
    def separate_flocking(self, vehicles):
        desiredseparation = self.radius * 2
        count = 0
        steer = PVector(0., 0.)
        for other in vehicles:
            if other.id == self.id: continue
            d = PVector.dist_s(self.location, other.location)
            if d > 0  and d < desiredseparation:
                diff = PVector.sub_s(self.location, other.location)
                diff.normalize()
                diff.div(d)
                steer.add(diff.x, diff.y)
                count += 1
        
        if count > 0:
            steer.div(count * 1.0)
        if steer.mag() > 0:
            steer.normalize()
            steer.mult(self.maxspeed)
            steer.sub(self.velocity.x, self.velocity.y)
            steer.limit(self.maxforce)
        return steer
    
    def align_flocking(self, vehicles):
        neighbordist = self.radius * 5
        count = 0
        sum = PVector(0., 0.)
        for other in vehicles:
            if other.id == self.id: continue
            d = PVector.dist_s(self.location, other.location)
            if d > 0  and d < neighbordist:
                sum.add(other.velocity.x, other.velocity.y)
                count += 1
        if count > 0:
            sum.div(count * 1.0)
            sum.normalize()
            sum.mult(self.maxspeed)
            steer = PVector.sub_s(sum, self.velocity)
            steer.limit(self.maxforce)
            return steer
        else: return PVector(0., 0.)
            
    def cohesion_flocking(self, vehicles):
        neighbordist = self.radius * 5
        count = 0
        sum = PVector(0., 0.)
        for other in vehicles:
            if other.id == self.id: continue
            d = PVector.dist_s(self.location, other.location)
            if d > 0  and d < neighbordist:
                sum.add(other.location.x, other.location.y)
                count += 1
        if count > 0:
            sum.div(count * 1.0)
            return self.seek(sum)
        else: return PVector(0., 0.)
    
    def applyForce(self, force):
        self.acceleration.add(force.x, force.y) # 将力转化为加速度

    def update(self):
        self.velocity.add(self.acceleration.x, self.acceleration.y)
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity.x, self.velocity.y)
        self.borders()
        self.acceleration.mult(0)  

    def getNormalPoint(self, p, a, b):
        ap = PVector.sub_s(p, a)
        ab = PVector.sub_s(b, a)
        ab.normalize()
        ab.mult(ap.dot(ab))
        normalPoint = PVector.add_s(a, ab)
        return normalPoint

    def borders(self):
        if self.location.x < -self.r:
            self.location.x = ENV_W + self.r
        if self.location.y < -self.r:
            self.location.y = ENV_H + self.r
        if self.location.x > ENV_W + self.r:
            self.location.x = -self.r
        if self.location.y > ENV_H + self.r:
            self.location.y = -self.r

    # 计算车辆方向坐标，用于绘制
    def coords(self):
        angle = self.velocity.heading() - 3.1415926 / 2
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)

        new_points = []
        for x_old, y_old in self.points:
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append(x_new + self.location.x)
            new_points.append(y_new + self.location.y)
        return new_points

