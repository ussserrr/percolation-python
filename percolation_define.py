#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np

import matplotlib.pyplot as plt

from percolation import print_clusters


# parameters
grid_x_dimension = 5
grid_y_dimension = 5
probability_of_zero = 0.5


# form the grid (with borders of zeros)
grid = np.zeros((grid_y_dimension+2, grid_x_dimension+2))

# fill the grid
for cell in np.nditer(grid[1:-1, 1:-1], op_flags=['readwrite']):
    cell[...] = 0 if np.random.random()<probability_of_zero else 1

num_of_ones = np.count_nonzero(grid)

# show grid (without borders of zeros)
plt.matshow(grid[1:-1, 1:-1], cmap=plt.cm.gray_r)
plt.show()


# at start all filled cells has uniq IDs (starting from 0)
cells_clusters_ids = np.arange(num_of_ones)  # cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)
cells_of_clusters = [list(x) for x in np.argwhere(grid>0)]  # координаты занятых ячеек


# обходим занятые ячейки начиная с левого верхнего угла и меняем метку кластера текущей ячейки
# на основе меток предыдущих (по вертикали и горизонтали) ближайших соседей
while True:
    cw = []  # массив правильных и неправильных меток

    for i in np.arange(num_of_ones):
        y,x = cells_of_clusters[i]

        # если хотя бы один из соседей заполнен, меняем текущую метку (ID) текущей ячейки
        # на метку этого соседа (поэтому сначала ищем этого соседа по известным координатам)
        if grid[y-1][x]==1 and grid[y][x-1]==0:
            cells_clusters_ids[i] = cells_clusters_ids[cells_of_clusters.index([y-1,x])]
        elif grid[y][x-1]==1 and grid[y-1][x]==0:
            cells_clusters_ids[i] = cells_clusters_ids[cells_of_clusters.index([y,x-1])]

        # если оба соседа заполнены, ищем метки их кластеров и для рассматриваемой ячейки
        # меняем метку на минимальную из меток соседей
        elif grid[y-1][x]==1 and grid[y][x-1]==1:
            id_of_first_neighbor = cells_clusters_ids[cells_of_clusters.index([y-1,x])]
            id_of_second_neighbor = cells_clusters_ids[cells_of_clusters.index([y,x-1])]
            cells_clusters_ids[i] = np.min([id_of_first_neighbor, id_of_second_neighbor])

            # если метки соседей различны, сохраняем их для последующего исправления
            if id_of_first_neighbor!=id_of_second_neighbor:
                cw.append([id_of_first_neighbor,id_of_second_neighbor])

    # если больше нет различных меток в пределах одного кластера, завершаем итерации
    if cw==[]:
        break
    # иначе исправляем бОльшие метки на мЕньшие и повторяем обход
    else:
        for id1,id2 in cw:
            wrong_id = np.max([id1,id2])
            correct_id = np.min([id1,id2])
            cells_clusters_ids[cells_clusters_ids==wrong_id] = correct_id


# print ids to see how the algorithm number them
table = print_clusters(grid, cells_clusters_ids, grid_y_dimension, grid_x_dimension)
plt.table(cellText=table)
plt.axis('off')


# координаты ячеек каждого кластера, unique - выборка из всех уникальных меток кластеров
clusters_coordinates = []
for idx in np.unique(cells_clusters_ids):
    clusters_coordinates.append([
        cells_of_clusters[k]
        for k in range(len(cells_clusters_ids))
        if cells_clusters_ids[k]==idx
        ])

    # поиск соединяющего кластера
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


plt.show()
