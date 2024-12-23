# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:32:53 2024

@author: SN -> Acknowledgments to the appropriate parties
"""

from threading import Thread
import time
import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import glob

class Omnirobot:
     def __init__(self,path = "", color = None):
          self.color = color
          self.path = path
          filenames = glob.glob(self.path+"/*.stl")
          self.robot = []
          self.robotCopy = []
          self.isTrajectory = False
          
          for filename in filenames:
             self.robot.append(pv.PolyData(filename))
             self.robotCopy.append(pv.PolyData(filename))
    
     def configureScene(self, bounds, window_size = [1024, 1024], title = "Robot omnidireccional"):
          self.bounds = bounds
          self.plotter = BackgroundPlotter(title=title)
          self.plotter.set_background(color='white')
          
     def initRobot(self, x1, y1, phi, escala):          
          self.x1, self.y1, self.phi= x1, y1, phi
          self.escala = escala
          
          for i in range(len(self.robot)):
               self.robot[i].points *= self.escala
               self.robotCopy[i].points *= self.escala
               if self.color == None:
                    self.plotter.add_mesh(self.robotCopy[i], 'black')
               else:
                    self.plotter.add_mesh(self.robotCopy[i], self.color[i])

     def initTrajectory(self, hx, hy):
          self.isTrajectory = True
          self.hx, self.hy = hx, hy
          self.sizeh = len(self.hx)
          points = np.column_stack((np.zeros(self.sizeh),np.zeros(self.sizeh),np.zeros(self.sizeh)))
          self.spline = pv.Spline(points,self.sizeh)
          self.plotter.add_mesh(self.spline,color='red',line_width = 4)

     def plotDesiredTrajectory(self, hxd, hyd):
          sizehd = len(hxd)
          points = np.column_stack((hxd,hyd,np.zeros(sizehd)))
          self.spline1 = pv.Spline(points,sizehd)
          self.plotter.add_mesh(self.spline1,color='blue',line_width = 4)

     def startSimulation(self, step = 1, ts = 1):
          cpos = [(-8, -8, 8), # zoom x y z
                  (0.5, 0.5, 0.5), # Movimiento x y z
                  (0.28, 0.28, 0.28)]
          self.plotter.show_bounds(grid ='back', location = 'outer', color = '#000000', bounds = self.bounds,
                                   xlabel = 'x [m]', ylabel = 'y [m]', zlabel = 'z [m]')
          self.plotter.camera_position = cpos
          self.plotter.view_isometric()
          self.step = step
          self.ts = ts
          self.thread = Thread(target = self.simulation)
          self.thread.start()

     def simulation(self):
          for k in range(0,len(self.x1),self.step):
               if self.isTrajectory:
                    self.plotTrajectory(self.hx[k],self.hy[k],k)
               self.robotUniciclo(self.x1[k],self.y1[k],self.phi,k)
               time.sleep(self.ts)

     def robotUniciclo(self, x1, y1, phi, k):
        # Rotation matrix for the given angle phi
        Rz = np.array([[np.cos(phi), -np.sin(phi), 0],
                       [np.sin(phi),  np.cos(phi), 0],
                       [0, 0, 1]])
    
        for i in range(len(self.robotCopy)):
            # Reset to original points from self.robot
            self.robotCopy[i].points = self.robot[i].points.copy()            
            # Apply rotation
            self.robotCopy[i].points = (Rz @ self.robotCopy[i].points.T).T
            # Apply translation
            self.robotCopy[i].translate([x1, y1, 0], inplace=True)
               
     def plotTrajectory(self,hx,hy,k):
          self.spline.points[k:self.sizeh,0] = hx
          self.spline.points[k:self.sizeh,1] = hy
         
          
          
    

