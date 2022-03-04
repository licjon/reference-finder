from math import sqrt, pow, exp
 

def euclidean_distance(x, y):
    """ Return Euclidean distance between two lists.
        From https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python.
    """
    distance = sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))
    return 1 / exp(distance)
