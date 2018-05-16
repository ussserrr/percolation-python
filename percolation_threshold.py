#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

import matplotlib.pyplot as plt


# parameters
method = 'labels'  # 'labels' or 'graph'

#              y   x
grid_dims = [[10, 10],
             [15, 15],
             [20, 20]]

num_of_experiments = 100  # number of experiments for each probability

probability_step = 0.01


if method=='labels':
    from percolation import generate_grid, find_clusters, is_percolation
elif method=='graph':
    from percolation import generate_grid
    from percolation_graph import generate_graph, find_clusters, is_percolation


probability_of_zero_array = np.arange(probability_step, 1.0, probability_step)

for grid_y_dim,grid_x_dim in grid_dims:
    experiments_with_percolation_array = []

    for probability_of_zero in probability_of_zero_array:
        experiments_with_percolation = 0

        for experiment in range(num_of_experiments):
            grid = generate_grid(grid_y_dim, grid_x_dim, probability_of_zero)

            if method=='labels':
                coords,ids = find_clusters(grid)
                result = is_percolation(coords, ids, grid_y_dim, grid_x_dim)
            elif method=='graph':
                G = generate_graph(grid, grid_y_dim, grid_x_dim)
                clusters = find_clusters(grid, G)
                result = is_percolation(clusters, grid_y_dim, grid_x_dim)

            if result=='upwards' or result=='lefttoright' or result=='both':
                experiments_with_percolation += 1

        experiments_with_percolation_array.append(
            experiments_with_percolation/num_of_experiments)

        # display progress
        print('\r{}x{}: {:.2f}'.format(grid_x_dim, grid_y_dim, probability_of_zero), end='')
    print()

    plt.plot(probability_of_zero_array, experiments_with_percolation_array,
             label='{}x{}, N={}'\
             .format(grid_x_dim, grid_y_dim, num_of_experiments))


plt.legend()
plt.suptitle("Percolation threshold")
plt.xlabel("Probability of 0")
plt.ylabel("Percolation ratio")

plt.show()
