# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:46:18 2025

@author: Rodolfo Alberto Reyes Corona
"""

import numpy as np
from pso import ParticleSwarmOptimizer

class Ant:
    def __init__(self, initial_point):
        self.initial_point = initial_point
        self.reset()
        
    def move_to(self, new_node, distance):
        self.path.append(new_node)
        self.cost += distance

    def reset(self):
        self.path = [self.initial_point]
        self.cost = 0

    def get_path(self):
        return self.path

    def get_cost(self):
        return self.cost

class ACO_PSO:
    def __init__(self, initial_point, final_point, n_ants, n_iterations, size):
        """
        Args:
            initial_point (list): Bidimensional initial point
            final_point (list): Bidimensional final point
            n_ants (int): Number of ants running per iteration
            n_iterations (int): Maximum number of iterations
            learning_rate (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, 
                    so 0.95 will lead to decay, 0.5 to much faster decay.
            size (int): This number provide the size of the resolution space in a quad area.
            alpha (int or float): Exponenet on pheromone, higher alpha gives pheromone more weight. Firs iteration = random
            beta (int or float): Exponent on distance, higher beta give distance more weight. First iteration = random
        Example:
            hybrid_algorithm = ACO_PSO([0,0], [5,5], 100, 10, 10)
        """ 
        self.initial_point = initial_point
        self.final_point = final_point
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.learning_rate = 0.95
        self.size = size
        self.table = {}
        self.best_path = None
        self.best_length = np.inf
        self.alpha = np.random.uniform(0,1)
        self.beta  = np.random.uniform(0,1)

        x_i, x_f = 0, self.size[0] + 0.01
        y_i, y_f = 0, self.size[1] + 0.01
        x = list(np.arange(x_i, x_f, 0.5))
        y = list(np.arange(y_i, y_f, 0.5))  
        self.X, self.Y = np.meshgrid(x, y)

    def euclidean_distance(self, point_1, point_2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2
        d = (x_2 - x_1) ** 2 + (y_2 - y_1) ** 2
        return np.sqrt(d)

    # Esta función proporciona los nodos posibles en una relación de distancia mínima
    def possible_options_nodes(self, node):
        min_distance = 0.8  # Ajusté la distancia mínima a 0.707 (aproximadamente sqrt(2) * 0.5)
        options = []
        for i in range(self.X.shape[0]):  # Cambié self.size[0] a self.X.shape[0] para asegurarme de iterar sobre la malla
            for j in range(self.Y.shape[1]):  # Igual para el eje Y
                possible_new_node = [self.X[i, j], self.Y[i, j]]
                distance = self.euclidean_distance(node, possible_new_node)
                if 0 < distance <= min_distance:  # Comprobamos que la distancia sea mayor que 0 y menor o igual a min_distance
                    options.append(possible_new_node)
        return options    

    # Choose new node function provide a new node based in the probability equation.
    def choose_new_node(self, node, nodes_options, pheromones, alpha, beta):
        probabilities = []
        for i, node_option in enumerate(nodes_options):
            distance = self.euclidean_distance(node, node_option)
            visibility = 1 / distance
            pheromone = pheromones[i]
            probabilities.append((pheromone ** beta) * (visibility ** alpha))

        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()
        cumulative_prob = np.cumsum(probabilities)
        rng = np.random.uniform(0, 1)
        return nodes_options[np.searchsorted(cumulative_prob, rng)]

    def get_pheromones(self, options, node):
        pheromones = []
        for option in options:
            possible_route = (tuple(node), tuple(option))
            pheromones.append(self.table.get(possible_route, 0.01))
        return pheromones

    def actualization(self, pheromones, ants):
        rho = 0.1
        for route, pheromone in self.table.items():
            new_pheromone = (1 - rho) * pheromone
            for ant in ants:
                ant_path = ant.get_path()
                for j in range(len(ant_path) - 1):
                    route_aux = (tuple(ant_path[j]), tuple(ant_path[j + 1]))
                    if route == route_aux:
                        new_pheromone += self.learning_rate / ant.get_cost()
            self.table[route] = new_pheromone

    def initialize_ants(self):
        self.ants = [Ant(self.initial_point) for _ in range(self.n_ants)]

    def run_ACO_PSO(self):
        # Max step allowed for a better time response, this parameter you can modify.
        max_step = 250
        self.initialize_ants()

        # Particle Swarm Optimization (PSO) initialization parameters.       
        num_particles = 300
        num_iterations = 100
        var_min = 0
        var_max = 1
        variables = 2
        
        for it in range(self.n_iterations):
            for h, ant in enumerate(self.ants):
                print(f'\rExecuting the iteration {(it + 1):04} of {str(self.n_iterations).zfill(4)}. Ant: {str(h + 1).zfill(4)} / {str(self.n_ants).zfill(4)}', end='')            
                ant.reset()
                actual_node = self.initial_point
                step = 0
                previous_node = []
                
                while True:
                    # Search possible options nodes
                    options = self.possible_options_nodes(actual_node)
                    if(step > 1):
                        for option in options:
                            if(option == previous_node):
                                options.remove(option)
                    
                    # Get the value of the pheromones
                    pheromones = self.get_pheromones(options, actual_node)
                    # Choose a new node using the possible optines and values
                    new_node = self.choose_new_node(actual_node, options, pheromones, self.alpha, self.beta)
                    previous_node = actual_node
                    distance = self.euclidean_distance(actual_node, new_node)
                    ant.move_to(new_node, distance)
                    actual_node = new_node
                    step += 1

                    if actual_node == self.final_point or step == max_step:
                        break
    
                # We verify the best cost based on path and lenght
                if ant.get_cost() < self.best_length:
                    self.best_length = ant.get_cost()
                    self.best_path = ant.get_path()
    
            # Actualization of the values.
            self.actualization(self.table, self.ants)
            
            # In this part, we need to verify if is the first iteration, this neccessary for PSO algorithm
            if it == 0:
                initial_cost = self.best_length
                current_cost = np.inf
            else:
                current_cost = self.best_length

            # The PSO algorithm is provided with a mathematical function and reaches its global minimum, however, 
            # here we do not have an associated function, so the results obtained in ACO are taken and in this way, 
            # it is assumed that it converged to the global minimum.
            optimizer = ParticleSwarmOptimizer(num_particles, num_iterations, var_min, var_max, variables, initial_cost, current_cost)
            optimizer.optimize()
            # We obtained the new values of alpha and beta
            self.beta, self.alpha = optimizer.get_best_position()            
        return self.ants
    
    def draw_ACOPSO2D(self, best_path, best_length):
        aux = [self.initial_point, self.final_point]
        import matplotlib.pyplot as plt

        x = [p[0] for p in best_path]
        y = [p[1] for p in best_path]
        
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b')
        for i, point in enumerate(aux):
            plt.text(point[0], point[1], f'{point}', fontsize=8, ha='right')

        plt.xlim(- 1, self.size[0] + 1)
        plt.ylim(- 1, self.size[1] + 1)
        plt.grid(True)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Path lenght ' + str(round(best_length,2)))
        plt.show()