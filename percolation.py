from random import random
from numpy import zeros, unique



def generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero):
    # form the grid (with borders of zeros)
    grid = zeros((grid_y_dimension+2,grid_x_dimension+2))

    # fill the grid
    for y in range(1, grid_y_dimension+1):
        for x in range(1, grid_x_dimension+1):
            if random()<probability_of_zero:
                grid[y][x] = 0
            else:
                grid[y][x] = 1

    return grid



def reset_clusters(grid, grid_y_dimension, grid_x_dimension):
    # at start all filled cells has uniq IDs (starting from 0)
    cells_clusters_ids = []  # cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)
    cells_of_clusters = []  # координаты занятых ячеек

    current_id = 0
    for y in range(1, grid_y_dimension+1):
        for x in range(1, grid_x_dimension+1):
            if grid[y][x]==1:
                cells_of_clusters.append([y,x])
                cells_clusters_ids.append(current_id)
                current_id = current_id+1

    return cells_of_clusters,cells_clusters_ids



def find_clusters(grid, cells_of_clusters, cells_clusters_ids):
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

    return cells_clusters_ids



def is_percolation(cells_clusters_ids, cells_of_clusters, grid_y_dimension, grid_x_dimension):
    """
    Defines whether there is a percolation in grid (grid_y_dimension X grid_x_dimension)
    and what its type.

    cells_clusters_ids
        cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)

    cells_of_clusters
        координаты занятых ячеек
        cells_clusters_ids и cells_of_clusters должны быть одного размера
    """

    # координаты каждого кластера, unique - выборка из всех уникальных меток кластеров
    clusters_coordinates = []
    col = 0
    for idx in unique(cells_clusters_ids):
        clusters_coordinates.append([])
        for k in range(len(cells_clusters_ids)):
            if cells_clusters_ids[k]==idx:
                clusters_coordinates[col].append(cells_of_clusters[k])
        col += 1

    # поиск соединяющего кластера
    upwards = False
    lefttoright = False
    for cluster in clusters_coordinates:
        y_array = []
        x_array = []
        for y,x in cluster:
            y_array.append(y)
            x_array.append(x)
        if (1 in y_array) and (grid_y_dimension in y_array):
            upwards = True
        if (1 in x_array) and (grid_x_dimension in x_array):
            lefttoright = True

    if upwards and not lefttoright:
        return 'upwards'
    elif not upwards and lefttoright:
        return 'lefttoright'
    elif upwards and lefttoright:
        return 'both'
    else:
        return 0



def print_clusters(grid, cells_clusters_ids, grid_y_dimension, grid_x_dimension,
                   fmt='{0:2d}', quiet=False):
    """
    Prints (if quiet=False) cells' clusters' IDs of grid (grid_y_dimension X grid_x_dimension)
    with fmt format in each cell. Returns this printed formatted list.
    """

    table = []
    row = 0
    i = 0
    for y in range(1, grid_y_dimension+1):
        table.append([])
        for x in range(1, grid_x_dimension+1):
            if grid[y][x]==1:
                table[row].append(fmt.format(cells_clusters_ids[i]))
                i += 1
            else:
                table[row].append(int(fmt[3])*' ')
        row += 1

    if not quiet:
        for row in table: print(row)

    return table
