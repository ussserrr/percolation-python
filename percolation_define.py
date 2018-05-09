from random import random
from numpy import zeros
import matplotlib.pyplot as plt

from percolation import is_percolation, print_clusters


# parameters
grid_x_dimension = 10
grid_y_dimension = 10
probability_of_zero = 0.5


# form the grid (with borders of zeros)
grid = zeros((grid_y_dimension+2, grid_x_dimension+2))

# fill the grid
for y in range(1, grid_y_dimension+1):
    for x in range(1, grid_x_dimension+1):
        if random()<probability_of_zero:
            grid[y][x] = 0
        else:
            grid[y][x] = 1


# show grid (without borders)
plt.matshow([row[1:-1] for row in grid[1:-1]], fignum=0, cmap=plt.cm.gray_r)
plt.xticks(range(grid_x_dimension), range(1, grid_x_dimension+1))
plt.yticks(range(grid_y_dimension), range(1, grid_y_dimension+1))
plt.show()


# at start all filled cells has uniq IDs (starting from 0)
cells_clusters_ids = []  # cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)
cells_of_clusters = []  # координаты занятых ячеек
idx = 0
for y in range(1, grid_y_dimension+1):
    for x in range(1, grid_x_dimension+1):
        if grid[y][x]==1:
            cells_of_clusters.append([y,x])
            cells_clusters_ids.append(idx)
            idx += 1


# обходим занятые ячейки начиная с левого верхнего угла и меняем метку кластера текущей ячейки
# на основе меток предыдущих (по вертикали и горизонтали) ближайших соседей
range_len_cells_clusters_ids = range(len(cells_clusters_ids))
while True:
    np = []  # массив правильных и неправильных меток

    for i in range_len_cells_clusters_ids:
        y = cells_of_clusters[i][0]
        x = cells_of_clusters[i][1]

        # если хотя бы один из соседей заполнен, меняем текущую метку (ID) текущей ячейки
        # на метку этого соседа (поэтому сначала ищем этого соседа по известным координатам)
        if grid[y-1][x]==1 and grid[y][x-1]==0:
            for k in range_len_cells_clusters_ids:
                if cells_of_clusters[k]==[y-1,x]:
                    cells_clusters_ids[i] = cells_clusters_ids[k]
        elif grid[y][x-1]==1 and grid[y-1][x]==0:
            for k in range_len_cells_clusters_ids:
                if cells_of_clusters[k]==[y,x-1]:
                    cells_clusters_ids[i] = cells_clusters_ids[k]

        # если оба соседа заполнены, ищем метки их кластеров и для рассматриваемой ячейки
        # меняем метку на минимальную из меток соседей
        elif grid[y-1][x]==1 and grid[y][x-1]==1:
            for k in range_len_cells_clusters_ids:
                if cells_of_clusters[k]==[y-1,x]:
                    id_of_first_neighbor = cells_clusters_ids[k]
                if cells_of_clusters[k]==[y,x-1]:
                    id_of_second_neighbor = cells_clusters_ids[k]
            cells_clusters_ids[i] = min(id_of_first_neighbor, id_of_second_neighbor)
            # если метки соседей различны, сохраняем их для последующего исправления
            # в следующей итерации while
            if id_of_first_neighbor!=id_of_second_neighbor:
                np.append([id_of_first_neighbor,id_of_second_neighbor])

    # если больше нет различных меток в пределах одного кластера, завершаем итерации
    if np==[]:
        break
    # иначе исправляем бОльшие метки на мЕньшие и повторяем обход
    else:
        for id1,id2 in np:
            wrong_id = max(id1,id2)
            right_id = min(id1,id2)
            for i in range_len_cells_clusters_ids:
                if cells_clusters_ids[i]==wrong_id:
                    cells_clusters_ids[i] = right_id


table = print_clusters(grid, cells_clusters_ids, grid_y_dimension, grid_x_dimension)
plt.table(cellText=table)
plt.axis('off')


result = is_percolation(cells_clusters_ids, cells_of_clusters, grid_y_dimension, grid_x_dimension)

if result=='upwards':
    print("There is an upwards percolation")
elif result=='lefttoright':
    print("There is a percolation from left to right")
elif result=='both':
    print("There is an upwards percolation")
    print("There is a percolation from left to right")
else:
    print("There is no percolation")


plt.show()
