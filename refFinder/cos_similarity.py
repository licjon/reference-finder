import warnings

from math import sqrt

def squared_sum(x):
  """ Return 3 rounded square rooted value. """
  return round(sqrt(sum([a * a for a in x])), 3)


def cos_similarity(x,y):
  """ Return cosine similarity between two lists.
      Exact match has score of 1.0.
  """
  numerator = sum(a * b for a, b in zip(x, y))
  denominator = squared_sum(x) * squared_sum(y)

  # TODO fix division by zero problem
  with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      # print(str(denominator))
      return round(numerator / float(denominator), 3)
