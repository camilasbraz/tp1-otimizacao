import numpy as np

def bit2num(bit, range):
  """Conversion from bit string representations to decimal numbers.

  Args:
    bit: bit string representation (a 0-1 vector)
    range: a two-element vector specifying the range of the converted decimal number.

  Returns:
    num: the converted decimal number
  """

  integer = np.polyval(bit, 2)
  num = integer * ((range[1] - range[0]) / (2**len(bit) - 1)) + range[0]
  return num
