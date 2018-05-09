#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import networkx as nx

import matplotlib.pyplot as plt

import numpy as np

from percolation import generate_grid


grid_x_dimension = 5
grid_y_dimension = 5
probability_of_zero = 0.5


grid = generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero)
plt.matshow( [row[1:-1] for row in grid[1:-1]], fignum=0, cmap=plt.cm.gray_r )


# every occupied cell is a graph node
G = nx.Graph()
idx = 0
for y in range(1, grid_y_dimension+1):
    for x in range(1, grid_x_dimension+1):
        if grid[y][x]==1:
            G.add_node(idx, coords=[y,x])

            if grid_x_dimension<=11 and grid_y_dimension<=11:
                plt.annotate( '{}'.format(idx), xy=(x-1,y-1), color='white',
                              horizontalalignment='center', verticalalignment='center' )

            idx += 1


# connect (add edges) neighboring nodes (i.e. neighboring occupied cells) to one cluster
num_of_ones = len(G)
for i in range(num_of_ones):
    y = G.nodes[i]['coords'][0]; x = G.nodes[i]['coords'][1]

    if grid[y-1][x]==1:
        for node in G.nodes.items():
            if node[1]['coords']==[y-1,x]:
                G.add_edge( i, node[0] )

    if grid[y][x-1]==1:
        for node in G.nodes.items():
            if node[1]['coords']==[y,x-1]:
                G.add_edge( i, node[0] )


# select clusters (subgraphs) from graph to define percolation and its type
highlighted_cells = np.zeros((grid_y_dimension,grid_x_dimension))

for cluster in nx.connected_component_subgraphs(G):
    # Transform coordinates array to find cluster's items at both bounds
    #
    #    x y
    #   [0,1]      xs [0,2,4]
    #   [2,3]  =>  ys [1,3,5].
    #   [4,5]
    #
    coords = np.array([ node[1]['coords'] for node in cluster.nodes.items() ])
    coords_ys_xs = coords.T

    ys = coords_ys_xs[0]; xs = coords_ys_xs[1]

    if (1 in ys) and (grid_y_dimension in ys):
        print('upwards percolation')
        for y,x in coords:
            highlighted_cells[y-1][x-1] = 1

    if (1 in xs) and (grid_x_dimension in xs):
        print('left to right percolation')
        for y,x in coords:
            highlighted_cells[y-1][x-1] = 1

plt.matshow(highlighted_cells, fignum=0, cmap=plt.get_cmap('Reds'), alpha=0.5)
plt.show()


if grid_x_dimension<=11 and grid_y_dimension<=11:
    # show graph G structure
    nx.draw(G, with_labels=True, node_size=500, font_color='white')
    plt.show()
