# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:22:50 2024

@author: Rodolfo Alberto Reyes Corona
"""

import numpy as np

class Particle:
    def __init__(self, var_min, var_max, variables, initial_cost, current_cost):
        self.var_min = var_min
        self.var_max = var_max
        self.variables = variables

        self.position = np.random.uniform(var_min, var_max, variables)
        self.velocity = np.random.uniform(-1, 1, variables)
        self.best_position = self.position.copy()
        self.best_cost = initial_cost  # Inicializar el mejor costo con el valor proporcionado
        self.current_cost = initial_cost  # Inicializar el costo actual con el valor proporcionado

    def update(self, global_best_position, w, c1, c2):
        self.velocity = w * self.velocity + c1 * np.random.rand(self.variables) * (self.best_position - self.position) + c2 * np.random.rand(self.variables) * (global_best_position - self.position)
        self.position += self.velocity
        self.position = np.minimum(np.maximum(self.position, self.var_min), self.var_max)

        if self.current_cost < self.best_cost:
            self.best_cost = self.current_cost
            self.best_position = self.position.copy()

class ParticleSwarmOptimizer:
    def __init__(self, num_particles, num_iterations, var_min, var_max, variables, initial_cost, current_cost):
        self.particles = [Particle(var_min, var_max, variables, initial_cost, current_cost) for _ in range(num_particles)]
        self.global_best = min(self.particles, key=lambda x: x.best_cost)
        self.num_iterations = num_iterations
        self.w = 1.0
        self.c1 = 2.0
        self.c2 = 2.0
        self.particle_positions = []
        
    def optimize(self):
        for iteration in range(self.num_iterations):
            iteration_positions = []  # Lista para almacenar las posiciones de las partículas en la iteración actual

            for particle in self.particles:
                particle.update(self.global_best.best_position, self.w, self.c1, self.c2)
                iteration_positions.append(particle.position.copy())  # Guardar la posición actual de la partícula

            self.particle_positions.append(iteration_positions)  # Agregar la lista de posiciones en la iteración actual
            self.global_best = min(self.particles, key=lambda x: x.best_cost)
            
    def get_particle_positions(self):
        return self.particle_positions

    def get_best_position(self):
        return self.global_best.best_position
