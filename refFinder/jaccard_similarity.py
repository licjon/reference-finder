def jaccard_similarity(x, y):
  """ Takes 2 lists of string (sentences) and
      returns the jaccard similarity between two lists (float).
  """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality / float(union_cardinality)
