# --------------------------------------------------------------------------- #
#                             Percolation library                             #
# --------------------------------------------------------------------------- #


import numpy as np



def generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero):
    """
    Generate grid (grid_y_dimension X grid_x_dimension) (vertical X horizontal)
    and fill it with ones and zeros in accordance with the given probability of
    zero

    returns:
        numpy.array
    """

    # form the grid (with borders of zeros)
    grid = np.zeros((grid_y_dimension+2,grid_x_dimension+2))

    # fill the grid
    for cell in np.nditer(grid[1:-1, 1:-1], op_flags=['readwrite']):
        cell[...] = 0 if np.random.random()<probability_of_zero else 1

    return grid



def reset_clusters(grid, grid_y_dimension, grid_x_dimension):
    """

    """

    # at start all filled cells has uniq IDs (starting from 0)
    num_of_ones = np.count_nonzero(grid)
    ids = np.arange(num_of_ones)  # cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)

    coords = [list(x) for x in np.argwhere(grid>0)]  # координаты занятых ячеек

    return coords,ids



def find_clusters(grid, coords, ids):
    """
    Define individual clusters (i.e. neighboring occupied cells) by iterating
    through the grid and labeling such cells by same IDs

    inputs:
        ids
        array of initial

    returns:

    """

    # обходим занятые ячейки начиная с левого верхнего угла и меняем метку кластера текущей ячейки
    # на основе меток предыдущих (по вертикали и горизонтали) ближайших соседей
    while True:
        cw = []  # массив правильных и неправильных меток

        for i in np.arange(ids.size):
            y,x = coords[i]

            # если хотя бы один из соседей заполнен, меняем текущую метку (ID) текущей ячейки
            # на метку этого соседа (поэтому сначала ищем этого соседа по известным координатам)
            if grid[y-1][x]==1 and grid[y][x-1]==0:
                ids[i] = ids[coords.index([y-1,x])]
            elif grid[y][x-1]==1 and grid[y-1][x]==0:
                ids[i] = ids[coords.index([y,x-1])]

            # если оба соседа заполнены, ищем метки их кластеров и для рассматриваемой ячейки
            # меняем метку на минимальную из меток соседей
            elif grid[y-1][x]==1 and grid[y][x-1]==1:
                first_neighbor_id = ids[coords.index([y-1,x])]
                second_neighbor_id = ids[coords.index([y,x-1])]
                ids[i] = np.min([first_neighbor_id, second_neighbor_id])

                # если метки соседей различны, сохраняем их для последующего исправления
                if first_neighbor_id!=second_neighbor_id:
                    cw.append([first_neighbor_id,second_neighbor_id])

        # если больше нет различных меток в пределах одного кластера, завершаем итерации
        if cw==[]:
            break
        # иначе исправляем бОльшие метки на мЕньшие и повторяем обход
        else:
            for id1,id2 in cw:
                wrong_id = np.max([id1,id2])
                correct_id = np.min([id1,id2])
                ids[ids==wrong_id] = correct_id

    return ids



def is_percolation(ids, coords, grid_y_dimension, grid_x_dimension):
    """
    Defines whether there is a percolation in grid (grid_y_dimension X grid_x_dimension)
    and what its type.

    ids
        cells' clusters' IDs (идентификаторы (метки) кластеров ячеек)

    coords
        координаты занятых ячеек
        ids и coords должны быть одного размера
    """

    # координаты ячеек каждого кластера, unique - выборка из всех уникальных меток кластеров
    clusters_coordinates = []
    for idx in np.unique(ids):
        clusters_coordinates.append([
            coords[k] for k in range(len(ids)) if ids[k]==idx
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
        return 'upwards'
    elif not upwards and lefttoright:
        return 'lefttoright'
    elif upwards and lefttoright:
        return 'both'
    else:
        return 0



def print_clusters( grid, ids, grid_y_dimension, grid_x_dimension,
                    fmt='{0:2d}', quiet=False ):
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
                table[row].append(fmt.format(ids[i]))
                i += 1
            else:
                table[row].append(int(fmt[3])*' ')
        row += 1

    if not quiet:
        for row in table: print(row)

    return table
