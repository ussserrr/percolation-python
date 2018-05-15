#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

import matplotlib.pyplot as plt


# parameters
method = 'labels'  # 'labels' or 'graph'

grid_x_dimension = 10
grid_y_dimension = 10

N = 10  # number of experiments for each probability

probability_step = 0.01


if method=='labels':
    from percolation import generate_grid, reset_clusters, find_clusters, is_percolation
elif method=='graph':
    from percolation import generate_grid
    from percolation_graph import generate_graph, find_clusters, is_percolation


probability_of_zero_array = np.arange(probability_step, 1.0, probability_step)
experiments_with_percolation_array = []

for probability_of_zero in probability_of_zero_array:
    experiments_with_percolation = 0

    for experiment in range(N):
        if method=='labels':
            grid = generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero)
            cells_of_clusters,cells_clusters_ids = reset_clusters(grid, grid_y_dimension, grid_x_dimension)
            cells_clusters_ids = find_clusters(grid, cells_of_clusters, cells_clusters_ids)
            result = is_percolation(cells_clusters_ids, cells_of_clusters, grid_y_dimension, grid_x_dimension)
        elif method=='graph':
            grid = generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero)
            G = generate_graph(grid, grid_y_dimension, grid_x_dimension)
            clusters = find_clusters(grid, G)
            result = is_percolation(clusters, grid_y_dimension, grid_x_dimension)

        if result=='upwards' or result=='lefttoright' or result=='both':
            experiments_with_percolation += 1

    experiments_with_percolation_array.append(experiments_with_percolation/N)

    print('\r{0:0.2f}'.format(probability_of_zero), end='')  # progress


plt.plot(probability_of_zero_array, experiments_with_percolation_array)

plt.title("Percolation threshold")
plt.xlabel("Probability of 0")
plt.ylabel("Percolation ratio")

plt.show()
