import numpy as np
import matplotlib.pyplot as plt

from nextpopu import nextpopu
from bit2num import bit2num
from evalpopu import evalpopu, evaleach
from function_Ackley import function_Ackley
from function_peaks import function_peaks
from function_rastrigin import function_rastrigin

def lanca_GA_functions():
    # Clear all variables - Close all figures
    plt.close('all')

    # Number of generations
    generation_n = 40
    # Population size
    popuSize = 80
    # Crossover rate
    xover_rate = 0.70
    # Mutation rate
    mutate_rate = 0.03
    # Bit number for each input variable
    bit_n = 8

    # Global optimization method
    global OPT_METHOD
    OPT_METHOD = 'ga'

    # Objective function
    obj_fcn = function_peaks  # Change this to the desired objective function

    if obj_fcn == function_peaks:
        var_n = 2
        var_range = np.array([[-3, 3], [-3, 3]])
    elif obj_fcn == function_Ackley:
        var_n = 2
        var_range = np.array([[-35, 35], [-35, 35]])
    elif obj_fcn == function_rastrigin:
        var_n = 2
        var_range = np.array([[-5.12, 5.12], [-5.12, 5.12]])

    # Initial random population
    popu = np.random.rand(popuSize, bit_n * var_n) > 0.5

    # Initial vectors Best, Average, Poorest (zeros).
    upper = np.zeros(generation_n)
    average = np.zeros(generation_n)
    lower = np.zeros(generation_n)

    # If nplot = 2: Plot the population popu[xp;yp]
    nplot = 2  # Adjust this based on your needs or remove it if not needed

    # Main loop of GA
    for i in np.arange(generation_n):
        # Evaluate objective function for each individual
        fcn_value = evalpopu(popu, bit_n, var_range, obj_fcn, nplot)
        if i == 0:
            print('Initial population.')

        # Fill objective function matrices (Best, Average, Poorest)
        upper[i] = max(fcn_value)
        average[i] = np.mean(fcn_value)
        lower[i] = min(fcn_value)

        # Display current best
        best, index = max(fcn_value), np.argmax(fcn_value)
        print(f'Generation {i + 1}: f({bit2num(popu[index, :bit_n], var_range[0, :])}, '
              f'{bit2num(popu[index, bit_n:2 * bit_n], var_range[1, :])}) = {best}')

        # Generate next population via selection, crossover, and mutation
        popu = nextpopu(popu, fcn_value, xover_rate, mutate_rate)

    plt.figure(3)
    x = np.arange(1, generation_n + 1)
    plt.plot(x, upper, 'o', x, average, 'x', x, lower, '*')
    plt.plot(x, upper, '-', x, average, '-', x, lower, '-')
    plt.legend(['Best', 'Average', 'Poorest'])
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.show()

lanca_GA_functions()
