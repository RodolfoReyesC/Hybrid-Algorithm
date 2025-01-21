# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:46:18 2025

@author: Rodolfo Alberto Reyes Corona
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AnimationACO:
    def __init__(self, paths, offsets, colors=None, interval=50):
        """
        Inicializa la animación de las trayectorias.
        
        :param paths: Lista de trayectorias, cada una es una lista de puntos (x, y).
        :param offsets: Lista de offsets (en frames) para cada trayectoria.
        :param colors: Lista de colores para cada trayectoria.
        :param interval: Intervalo entre frames en milisegundos.
        """
        self.paths = paths
        self.offsets = offsets
        self.colors = colors if colors else ['red', 'blue', 'green']
        self.interval = interval
        self.num_points = 500
        self.total_frames = self.num_points + max(self.offsets)
        self.interpolated_paths = self._interpolate_paths()
        
        # Configuración de la figura
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-1, 3)
        self.ax.set_ylim(-1, 5)
        self.ax.grid('True')
        
        # Crear las líneas y puntos para cada trayectoria
        self.lines = [self.ax.plot([], [], color=color, lw=2)[0] for color in self.colors]
        self.points = [self.ax.plot([], [], 'o', color=color)[0] for color in self.colors]
        
        # Crear la animación
        self.anim = FuncAnimation(
            self.fig, self._update, frames=self.total_frames, interval=self.interval, blit=True
        )

    def _interpolate_paths(self):
        """
        Interpola las trayectorias para tener el mismo número de puntos.
        
        :return: Lista de trayectorias interpoladas (x, y).
        """
        interpolated = []
        for path in self.paths:
            distances = [np.sqrt((path[i][0] - path[i - 1][0])**2 + (path[i][1] - path[i - 1][1])**2)
                         for i in range(1, len(path))]
            total_length = sum(distances)
            t = [0]
            for d in distances:
                t.append(t[-1] + d / total_length)
            t = np.array(t)  # Normalizado a [0, 1]
            
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
        Actualiza las posiciones de las líneas y puntos en cada frame.
        
        :param frame: Frame actual de la animación.
        :return: Lista de objetos actualizados.
        """
        if frame >= self.offsets[2] + self.num_points - 1:
            self.anim.event_source.stop()  # Detener la animación

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
        """Muestra la animación."""
        plt.show()