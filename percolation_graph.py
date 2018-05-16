# --------------------------------------------------------------------------- #
#                     Percolation library (graph edition)                     #
# --------------------------------------------------------------------------- #


import numpy as np

import networkx as nx



def generate_graph(grid, grid_y_dimension, grid_x_dimension):
    """
    Generate graph where each node represent one occupied cell of the grid

    returns:
        networkx.Graph instance
    """

    G = nx.Graph()

    idx = 0
    for y in range(1, grid_y_dimension+1):
        for x in range(1, grid_x_dimension+1):
            if grid[y][x]==1:
                G.add_node(idx, coords=[y,x])
                idx += 1

    return G



def find_clusters(grid, graph):
    """
    Create connections (graph edges) between nodes (neighboring occupied cells)

    returns:
        array of subgraphs representing individual clusters
    """

    num_of_ones = len(graph)
    for i in range(num_of_ones):
        # extract coordinates
        y,x = graph.nodes[i]['coords'][0], graph.nodes[i]['coords'][1]

        if grid[y-1][x]==1:
            for node in graph.nodes.items():
                if node[1]['coords']==[y-1,x]:
                    graph.add_edge( i, node[0] )

        if grid[y][x-1]==1:
            for node in graph.nodes.items():
                if node[1]['coords']==[y,x-1]:
                    graph.add_edge( i, node[0] )

    return nx.connected_component_subgraphs(graph)



def is_percolation(clusters, grid_y_dimension, grid_x_dimension):
    """
    Define whether there is a percolation and what its type

    input:
        clusters
        array of graphs representing clusters (neighboring occupied cells)
    """

    upwards_global = False
    lefttoright_global = False

    for cluster in clusters:
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

        if upwards and not lefttoright:
            upwards_global = True
        elif not upwards and lefttoright:
            lefttoright_global = True
        elif upwards and lefttoright:
            upwards_global = True
            lefttoright_global = True

    if upwards_global and not lefttoright_global:
        return 'upwards'
    elif not upwards_global and lefttoright_global:
        return 'lefttoright'
    elif upwards_global and lefttoright_global:
        return 'both'
    else:
        return 0
