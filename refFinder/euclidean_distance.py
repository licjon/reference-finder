from math import sqrt, pow, exp
 

def euclidean_distance(x, y):
    """ Return Euclidean distance between two lists. """
    distance = sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))
    return 1 / exp(distance)
