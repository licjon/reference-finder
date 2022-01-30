from math import sqrt
import warnings
 
def squared_sum(x):
  """ return 3 rounded square rooted value """
 
  return round(sqrt(sum([a*a for a in x])),3)

def cos_similarity(x,y):
  """ return cosine similarity between two lists """
 
  numerator = sum(a*b for a,b in zip(x,y))
  denominator = squared_sum(x)*squared_sum(y)

  # TODO fix division by zero problem
  with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      # print(str(denominator))
      return round(numerator/float(denominator),3)
