import matplotlib.pyplot as plt
from percolation import generate_grid, reset_clusters, find_clusters, is_percolation

# parameters
grid_x_dimension = 10
grid_y_dimension = 10
N = 10  # number of experiments for each probability
probability_step = 0.01


probability_of_zero = 1.0
experiments_with_percolation_array = []
probability_of_zero_array = []
while probability_of_zero>=0:
    experiments_with_percolation = 0

    for experiment in range(N):
        grid = generate_grid(grid_y_dimension, grid_x_dimension, probability_of_zero)
        cells_of_clusters,cells_clusters_ids = reset_clusters(grid, grid_y_dimension, grid_x_dimension)
        cells_clusters_ids = find_clusters(grid, cells_of_clusters, cells_clusters_ids)
        result = is_percolation(cells_clusters_ids, cells_of_clusters, grid_y_dimension, grid_x_dimension)

        if result=='upwards' or result=='lefttoright' or result=='both':
            experiments_with_percolation += 1


    experiments_with_percolation_array.append(experiments_with_percolation/N)
    probability_of_zero_array.append(probability_of_zero)
    print('\r{0:0.2f}'.format(probability_of_zero), end='')
    probability_of_zero -= probability_step


plt.plot(probability_of_zero_array, experiments_with_percolation_array)
plt.title("Порог перколяции")
plt.xlabel("Вероятность нуля")
plt.ylabel("Доля экспериментов с перколяцией")
plt.show()
