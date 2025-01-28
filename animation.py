# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:46:18 2025

@author: Rodolfo Alberto Reyes Corona
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationACO:
    def __init__(self, size, paths, lenghts, n_ants, n_iterations, offsets, colors=None, interval=50):
        """
        Initialize the animation of the trajectories.
        
        :param paths: List of trajectories, each being a list of points (x, y).
        :param offsets: List of offsets (in frames) for each trajectory.
        :param colors: List of colors for each trajectory.
        :param interval: Interval between frames in milliseconds.
        """
        self.size = size
        self.paths = paths
        self.lenghts = lenghts
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.offsets = offsets
        self.colors = colors if colors else ['red', 'blue', 'green']
        self.interval = interval
        self.num_points = 500
        self.total_frames = self.num_points + max(self.offsets)
        self.interpolated_paths = self._interpolate_paths()
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-0.5, self.size[0] + 0.5)
        self.ax.set_ylim(-0.5, self.size[1] + 0.5)
        self.ax.grid('True')

        self.lines = [self.ax.plot([], [], color=color, lw=2)[0] for color in self.colors]
        self.points = [self.ax.plot([], [], 'o', color=color)[0] for color in self.colors]
        self.ax.legend(['Robot 1 path lenght: ' + str(round(self.lenghts[0],2)), 'Robot 2 path length: ' + str(round(self.lenghts[1],2)), 'Robot 3 path length: ' + str(round(self.lenghts[2],2))], loc = 'upper right')
        self.ax.set_title('Comparation using ACO/PSO with ' + str(n_ants) + ' ants and ' + str(n_iterations) + ' iterations')
        
        self.anim = FuncAnimation(
            self.fig, self._update, frames=self.total_frames, interval=self.interval, blit=True
        )

    def _interpolate_paths(self):
        """
        Interpolate the trajectories to have the same number of points.
        
        :return: List of interpolated trajectories (x, y).
        """
        interpolated = []
        for path in self.paths:
            distances = [np.sqrt((path[i][0] - path[i - 1][0])**2 + (path[i][1] - path[i - 1][1])**2)
                         for i in range(1, len(path))]
            total_length = sum(distances)
            t = [0]
            for d in distances:
                t.append(t[-1] + d / total_length)
            t = np.array(t)  # Normalized to [0, 1]
            
            x = [p[0] for p in path]
            y = [p[1] for p in path]
            t = np.linspace(0, 1, len(path))
            t_interp = np.linspace(0, 1, self.num_points)
            x_interp = np.interp(t_interp, t, x)
            y_interp = np.interp(t_interp, t, y)
            interpolated.append((x_interp, y_interp))
        return interpolated

    def _update(self, frame):
        """
        Update the positions of the lines and points in each frame.
        
        :param frame: Current frame of the animation.
        :return: List of updated objects.
        """
        if frame >= self.offsets[2] + self.num_points - 1:
            self.anim.event_source.stop()  # Stop the animation

        for i, (line, point, (x, y), offset) in enumerate(
            zip(self.lines, self.points, self.interpolated_paths, self.offsets)
        ):
            if frame >= offset:
                relative_frame = frame - offset
                if relative_frame < len(x):
                    line.set_data(np.array(x[:relative_frame + 1]), np.array(y[:relative_frame + 1]))
                    point.set_data(np.array([x[relative_frame]]), np.array([y[relative_frame]]))
                else:
                    line.set_data(np.array(x), np.array(y))
                    point.set_data([], [])
        return self.lines + self.points

    def show(self):
        """Show the animation."""
        plt.show()