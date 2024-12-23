# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:27:03 2024

@author: Rodolfo Alberto Reyes Corona
"""

from aco_pso import ACO_PSO
import robot_ant as r_ant
# ----------------------------- ACO/PSO ----------------------------- #
initial_point = [0, 0]
final_point = [9,8]
n_ants = 350
n_iterations = 10
size = 10

aco_pso = ACO_PSO(initial_point, final_point, n_ants, n_iterations, size)
ants = aco_pso.run_ACO_PSO()
best_path, best_length = aco_pso.best_path, aco_pso.best_length

aco_pso.draw_ACO_PSO2D()
robots = r_ant.robot_ant(0.1, initial_point, final_point, size)
robots.draw_path(best_path)