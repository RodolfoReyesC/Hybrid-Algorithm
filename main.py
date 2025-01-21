# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:27:03 2024

@author: Rodolfo Alberto Reyes Corona
"""

from aco_pso import ACO_PSO
from animation import AnimationACO
# ----------------------------- ACO/PSO ----------------------------- #
initial_point = [0, 0]
final_point = [2,3.5]
n_ants = 100
n_iterations = 10
size = [2,4]

aco_pso = ACO_PSO(initial_point, final_point, n_ants, n_iterations, size)
ants = aco_pso.run_ACO_PSO()
# ------------------------- Pruebas con Vicon --------------------------- #
# Escogeremos 3 mejores opciones para así probar en 3 robots.
top_2_ants = sorted(ants, key=lambda ant: ant.cost)[:3]
ant1, ant2 = top_2_ants[0], top_2_ants[2]

aco_pso.draw_ACOPSO2D(ant1.path, ant1.cost)
aco_pso.draw_ACOPSO2D(ant2.path, ant2.cost)
aco_pso.draw_ACOPSO2D(aco_pso.best_path, aco_pso.best_length)

# --------------------- Animación de una vista 2D ------------------------ #
paths = [ant1.path, ant2.path, aco_pso.best_path]
offsets = [0, 100, 200]
animation = AnimationACO(paths, offsets)
animation.show()

