import numpy as np

def nextpopu(popu, fitness, xover_rate, mut_rate):
    # Check if the population is empty
    if popu.size == 0:
        raise ValueError("The population cannot be empty.")

    new_popu = np.copy(popu)
    popu_s = popu.shape[0]
    string_leng = popu.shape[1]

    # ELITISM: Find the best two and keep them
    tmp_fitness = np.copy(fitness)
    index1 = np.argmax(tmp_fitness)
    tmp_fitness[index1] = np.min(tmp_fitness)
    index2 = np.argmax(tmp_fitness)
    new_popu[0:2, :] = popu[[index1, index2], :]

    # Rescale the fitness
    fitness = fitness - np.min(fitness)
    total = np.sum(fitness)
    if total == 0:
        print(" === Warning: converge to a single point ===")
        fitness = np.ones(popu_s) / popu_s
    else:
        fitness = fitness / np.sum(fitness)
    cum_prob = np.cumsum(fitness)

    # SELECTION and CROSSOVER
    for i in range(1, popu_s // 2):
        # Select two parents based on their scaled fitness values
        tmp = np.where(cum_prob - np.random.rand() > 0)
        parent1 = popu[tmp[0][0], :]
        tmp = np.where(cum_prob - np.random.rand() > 0)
        parent2 = popu[tmp[0][0], :]

        # Do crossover
        if np.random.rand() < xover_rate:
            # Perform crossover operation
            xover_point = np.random.randint(1, string_leng)
            new_popu[i*2-1, :] = np.hstack((parent1[:xover_point], parent2[xover_point:]))
            new_popu[i*2, :] = np.hstack((parent2[:xover_point], parent1[xover_point:]))

    # MUTATION (elites are not subject to this)
    mask = np.random.rand(popu_s, string_leng) < mut_rate
    new_popu = np.logical_xor(new_popu, mask)

    # Restore the elites
    new_popu[0:2, :] = popu[[index1, index2], :]

    return new_popu