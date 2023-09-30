from bit2num import bit2num
import numpy as np

def evaleach(string, bit_n, var_range, fcn, nplot):
    """Evaluation of each individual's fitness value.

    Args:
        string: bit string representation of an individual
        bit_n: number of bits for each input variable
        var_range: range of input variables, a var_n by 2 matrix
        fcn: objective function (a Python function)
        nplot: plot the population popu[xp;yp]

    Returns:
        out: the fitness value of the individual
    """

    var_n = len(var_range)
    input_vars = np.zeros(var_n)

    for i in range(var_n):
        start = i * bit_n
        end = (i + 1) * bit_n
        input_vars[i] = bit2num(string[start:end], var_range[i])

    out = fcn(input_vars, nplot)
    return out
