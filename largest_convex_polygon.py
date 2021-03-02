import numpy as np
import cv2
import random

img = cv2.imread('img.jpg',cv2.IMREAD_COLOR)

pts = []

for i in range(40):#generate 40 random points
    pts.append((random.randint(0,500),random.randint(0,500)))

for i in pts:#draw the points on the image
    cv2.circle(img, i, 2, (0,0,0), -1)

class polygon:#the class that does all the work
    def __init__(self,points):
        self.points = points
        self.r_ex = (0,0)
        self.l_ex = (0,0)
        self.priority = True
        self.temp = {}
        
    def find_extreme(self):#finds the left and right most extreme points
        self.b = (0,0)#temperary storage variable
        for i in self.points:#just the max no algorithm
            if i[0] > self.b[0]:
                self.b = i
        self.l_ex = self.b
        for i in self.points:
            if i[0] < self.b[0]:
                self.b = i
        self.r_ex = self.b

    def find_points(self,point):#finds the point
        self.point = point
        self.m = -501#for a 500x500 image this is the minimum slope possible
        for i in self.points:
            if self.priority:#check if we have reached the left end
                if i[0] > self.point[0]:#calculate the slope and store it
                    self.m = float(i[1] - self.point[1])/float(i[0] - self.point[0])
                    self.temp[i] = self.m
                elif i[0] == self.point[0]:
                    if i[1] > self.point[1]:
                        self.m = 501
                        self.temp[i] = self.m
                    elif i[1] < self.point[1]:
                        self.m = -501
                        self.temp[i] = self.m
                    else:
                        pass
            if not self.priority:#same thing just in the opposite direction
                if i[0] < self.point[0]:
                    self.m = float(i[1] - self.point[1])/float(i[0] - self.point[0])
                    self.temp[i] = self.m
                elif i[0] == self.point[0]:
                    if i[1] > self.point[1]:
                        self.m = -501
                        self.temp[i] = self.m
                    elif i[1] < self.point[1]:
                        self.m = 501
                        self.temp[i] = self.m
                    else:
                        pass
        for i in self.temp.keys():#actually find the minimum slope point
            if self.m >= self.temp[i]:
                self.m = self.temp[i]
                self.point1 = i
        self.temp = {}
        return self.point1
    def draw_lines(self):#this one loops and draws the polygon
        self.lst = []
        self.point = self.r_ex
        while self.point != self.l_ex:
            self.point = self.find_points(self.point)
            self.lst.append(self.point)
        self.lst.append(self.l_ex)
        self.point = self.l_ex
        self.priority = False
        while self.point != self.r_ex:
            self.point = self.find_points(self.point)
            self.lst.append(self.point)
        self.lst.append(self.r_ex)
        for i in range(len(self.lst)):#to draw the polygon
            try:
                cv2.line(img,self.lst[i],self.lst[i+1],(0,0,255),1)
            except IndexError:
                cv2.line(img,self.lst[i],self.lst[0],(0,0,255),1)

x = polygon(pts)
x.find_extreme()
x.draw_lines()

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
