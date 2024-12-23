# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:42:37 2024

@author: rodo1
"""

import OmniRobot as pO
import numpy as np 

class robot_ant:
    def __init__(self, ts, point1, point2, size):
        """
        Args: 
            ts (int): Sampling time (s)
            point1 (list): Initial point for the trajectory.
            point2 (list): Final point in the trajectory
            size (int): This parameter define the size (LxL) for the solution space.
        """
        self.ts = ts
        self.point1 = point1
        self.point2 = point2
        self.size = size
        
    def draw_path(self, route):
        hx, hy, phi = [], [], 0
        # Generate points along the line from point0 to each point in points
        path = "stl"
        color = ["white", "blue"]
        omni3 = pO.Omnirobot(path,color)
        xmin, xmax = 0, self.size
        ymin, ymax = 0, self.size
        zmin, zmax = 0, 0
        bounds = [xmin, xmax, ymin, ymax, zmin, zmax]
        escala = 4
        omni3.configureScene(bounds)
        
        for point in route:
            dist = np.linalg.norm(np.array(point) - np.array(self.point1))
            steps = int(dist / 0.01)  # Adjust 0.01 for step size
            hx_aux = np.linspace(self.point1[0], point[0], steps)
            hy_aux = np.linspace(self.point1[1], point[1], steps)
            hx.extend(hx_aux)
            hy.extend(hy_aux)  
            self.point1 = point

        omni3.initTrajectory(hx,hy)
        omni3.initRobot(hx,hy,phi,escala)
        omni3.startSimulation(10,self.ts)