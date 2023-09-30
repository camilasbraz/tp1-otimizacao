from evaleach import evaleach
import numpy as np

def evalpopu(population, bit_n, var_range, fcn, nplot):
    """Evaluation of the population's fitness values.

    Args:
        population: 0-1 matrix of popu_n by string_leng
        bit_n: number of bits used to represent an input variable
        var_range: range of input variables, a var_n by 2 matrix
        fcn: objective function (a Python function)
        nplot: plot the population popu[xp;yp]

    Returns:
        fitness: a vector of fitness values
    """

    pop_n = population.shape[0]
    fitness = np.zeros(pop_n)
    for count in np.arange(pop_n):
        fitness[count] = np.sum(evaleach(population[count, :], bit_n, var_range, fcn, nplot))
    return fitness

