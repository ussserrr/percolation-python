#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import networkx as nx

import matplotlib.pyplot as plt

import numpy as np

from percolation import generate_grid


#
# Parameters
#
grid_x_dimension = 5
grid_y_dimension = 5

probability_of_zero = 0.4

# Maximal size to draw labels on cells (also defines the way to highlight
# clusters and displaying the graph, see below)
max_size = 11


#
# Generate and display grid via matplotlib
#
grid = generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero)
plt.matshow( grid[1:-1, 1:-1], fignum=0, cmap=plt.cm.gray_r )


#
# Create graph where each node represent one occupied cell of the grid. If the
# grid is not too big, put labels (IDs) over it
#
G = nx.Graph()
idx = 0
for y in range(1, grid_y_dimension+1):
    for x in range(1, grid_x_dimension+1):
        if grid[y][x]==1:
            G.add_node(idx, coords=[y,x])

            if grid_x_dimension<=max_size and grid_y_dimension<=max_size:
                plt.annotate( '{}'.format(idx), xy=(x-1,y-1), color='white',
                              horizontalalignment='center',
                              verticalalignment='center' )

            idx += 1


#
# Connect (add edges) neighboring nodes (i.e. neighboring occupied cells) to
# one cluster
#
num_of_ones = len(G)
for i in range(num_of_ones):
    # extract coordinates
    y,x = G.nodes[i]['coords'][0], G.nodes[i]['coords'][1]

    if grid[y-1][x]==1:
        for node in G.nodes.items():
            if node[1]['coords']==[y-1,x]:
                G.add_edge( i, node[0] )

    if grid[y][x-1]==1:
        for node in G.nodes.items():
            if node[1]['coords']==[y,x-1]:
                G.add_edge( i, node[0] )


#
# Define whether there is a percolation and what its type
#
cells_to_highlight = []

# This mode used for big grids (bigger than max_size for at least one dimension).
# plt.matshow() function colorizing cells based on their value so we can assign
# different values to each cluster and plt.matshow() will automatically
# highlight them for us. Because '0' and '1' already go for free and occupied
# cells respectively, this is a start value for enumerating
percolated_cluster_grid_value = 2

upwards_global = False
lefttoright_global = False

# select clusters (subgraphs) from graph
for cluster in nx.connected_component_subgraphs(G):
    upwards = False
    lefttoright = False

    # Transform coordinates array to find cluster's items at both bounds
    #
    #    x y
    #   [0,1]      xs [0,2,4]
    #   [2,3]  =>  ys [1,3,5]
    #   [4,5]
    #
    #  coords     coords_ys_xs
    #
    coords = np.array([ node[1]['coords'] for node in cluster.nodes.items() ])
    coords_ys_xs = coords.T

    ys = coords_ys_xs[0]; xs = coords_ys_xs[1]

    if (1 in ys) and (grid_y_dimension in ys):
        upwards = True
    if (1 in xs) and (grid_x_dimension in xs):
        lefttoright = True

    if upwards or lefttoright:
        for y,x in coords:
            grid[y][x] = percolated_cluster_grid_value
            cells_to_highlight.append([y,x])
        percolated_cluster_grid_value += 1

        if upwards and not lefttoright:
            upwards_global = True
        elif not upwards and lefttoright:
            lefttoright_global = True
        elif upwards and lefttoright:
            upwards_global = True
            lefttoright_global = True


if upwards_global and not lefttoright_global:
    print("There is an upwards percolation")
elif not upwards_global and lefttoright_global:
    print("There is a percolation from left to right")
elif upwards_global and lefttoright_global:
    print("There are both types of percolation")
else:
    print("There is no percolation")


#
# Highlight percolated clusters by one of two methods. If grid is big enough
# (bigger than max_size for at least one dimension), we colorize each percolated
# cluster using plt.matshow() (see percolated_cluster_grid_value), otherwise
# paint all percolated cluster in one color by putting another layer on it
#
if grid_x_dimension<=max_size and grid_y_dimension<=max_size:
    highlighted = np.zeros_like(grid)
    if cells_to_highlight != []:
        for y,x in cells_to_highlight:
            highlighted[y][x] = 1
    plt.matshow( highlighted[1:-1, 1:-1], fignum=0, cmap='Reds', alpha=0.5 )
else:
    plt.matshow( grid[1:-1, 1:-1] )
plt.suptitle("{}x{}, P(0)={:.2f}"\
             .format(grid_x_dimension, grid_y_dimension, probability_of_zero))
plt.show()


#
# Also show graph G structure for pretty small grids
#
if grid_x_dimension<=max_size and grid_y_dimension<=max_size:
    nx.draw(G, with_labels=True, node_size=500, font_color='white')
    plt.show()
