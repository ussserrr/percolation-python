#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

import matplotlib.pyplot as plt

from percolation import print_clusters


#
# Parameters
#
grid_x_dimension = 10
grid_y_dimension = 5
probability_of_zero = 0.4


#
# Generate grid (grid_y_dimension X grid_x_dimension) (vertical X horizontal)
# and fill it with ones and zeros in accordance with the given probability of
# zero. Also, we add borders of zeros to handle operations at edges (i.e.
# where (x-1)-like expressions could be met). For example, for 5x5 grid we
# will get:
#
#    array([[0., 0., 0., 0., 0., 0., 0.],
#           [0., 0., 1., 1., 1., 1., 0.],
#           [0., 1., 0., 0., 0., 1., 0.],
#           [0., 1., 1., 0., 0., 0., 0.],
#           [0., 1., 1., 0., 1., 0., 0.],
#           [0., 1., 1., 0., 1., 0., 0.],
#           [0., 0., 0., 0., 0., 0., 0.]])

# form the grid (with borders of zeros)
grid = np.zeros((grid_y_dimension+2, grid_x_dimension+2))

# fill the grid
for cell in np.nditer(grid[1:-1, 1:-1], op_flags=['readwrite']):
    cell[...] = 0 if np.random.random()<probability_of_zero else 1


#
# Show grid (without borders of zeros)
#
plt.matshow(grid[1:-1, 1:-1], cmap=plt.cm.gray_r)
plt.show()


#
# Find individual clusters (i.e. neighboring occupied cells) by iterating
# through the grid and reassigning cells' labels accordingly to their
# belonging to the same (or not) cluster
#
num_of_ones = np.count_nonzero(grid)

# 1-D array of labels (IDs) of each occupied cell. At the beginning,
# all labels are different and are simply counted like 0,1,2,3,...
ids = np.arange(num_of_ones)
# 2-D array that storing (y,x) coordinates of occupied cells
coords = [list(x) for x in np.argwhere(grid>0)]
# We operate with these two arrays in the parallel way so both ID and
# coordinates are always match to each other, e.g.:
#
#   id   y x
#    0  [2,0]
#    1  [2,3]
#    2  [4,5]
#      ...
#

# Reassign IDs (starting from the upper left corner) until there are no
# more left so called wrong labels - 'cw'. We change a label according to
# IDs of two closest neighboring cells (up and left ones)
while True:
    cw = []

    for i in np.arange(num_of_ones):
        # extract coordinates of an i-th current cell
        y,x = coords[i]

        # If only one neighbor is occupied, we change a label of the
        # current cell to the label of that neighbor. First, we need to
        # find ID of this neighbor by its known coordinates
        if grid[y-1][x]==1 and grid[y][x-1]==0:
            ids[i] = ids[coords.index([y-1,x])]
        elif grid[y][x-1]==1 and grid[y-1][x]==0:
            ids[i] = ids[coords.index([y,x-1])]

        # if both neighbors are occupied then we assign a smaller label
        elif grid[y-1][x]==1 and grid[y][x-1]==1:
            first_neighbor_id = ids[coords.index([y-1,x])]
            second_neighbor_id = ids[coords.index([y,x-1])]
            ids[i] = np.min([first_neighbor_id, second_neighbor_id])

            # if IDs are unequal then we store them to correct later
            if first_neighbor_id!=second_neighbor_id:
                cw.append([first_neighbor_id,second_neighbor_id])

    # quit the loop if there are no more wrong labels
    if cw==[]:
        break
    # else correct labels
    else:
        for id1,id2 in cw:
            wrong_id = np.max([id1,id2])
            correct_id = np.min([id1,id2])
            ids[ids==wrong_id] = correct_id


#
# Print IDs to see how the algorithm number them (using hand-made function and
# matplotlib)
#
table = print_clusters(grid, ids, quiet=False)
plt.table(cellText=table)
plt.axis('off')
plt.show()


#
# Define whether there is a percolation in the given grid and what its type.
# Correctly works only if find_clusters() function were called before
#
# ids contains labels of all occupied cells so we need to find uniq IDs
# (i.e. all remaining clusters), for example
#
#   ids = {0,0,0,0,1,2,2,0,0,3,3,3,5,5,2}  =>
#   np.unique(ids) = {0,1,2,3,5}
#
# Then we store coordinates of cells of all these clusters like
#
#   clusters_coordinates = [ [[1,2],  [[3,4],
#                             [2,2],   [3,5],
#                             [2,3]],  [4,5]] ]
#
clusters_coordinates = []
for idx in np.unique(ids):
    clusters_coordinates.append([
        coords[k]
        for k in range(len(ids))
        if ids[k]==idx
        ])

# search for percolated cluster(s)
upwards = False
lefttoright = False
for cluster in clusters_coordinates:
    cluster = np.array(cluster).T
    if (1 in cluster[0]) and (grid_y_dimension in cluster[0]):
        upwards = True
    if (1 in cluster[1]) and (grid_x_dimension in cluster[1]):
        lefttoright = True

if upwards and not lefttoright:
    print("There is an upwards percolation")
elif not upwards and lefttoright:
    print("There is a percolation from left to right")
elif upwards and lefttoright:
    print("There are both types of percolation")
else:
    print("There is no percolation")
