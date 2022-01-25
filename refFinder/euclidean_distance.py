import spacy
from math import sqrt, pow, exp
 
def squared_sum(x):
    """ return 3 rounded square rooted value """
 
    return round(sqrt(sum([a*a for a in x])), 3)
 
def euclidean_distance(x, y):
    """ Return Euclidean distance between two lists. """

    distance = sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))
    return 1/exp(distance)
