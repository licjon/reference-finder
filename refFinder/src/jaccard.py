from itertools import zip_longest


def get_jaccard_top_score(ms_sentence, ref_sentences, ref_word_sentences):
    scores = []
    """ Return the sentence with the highest Jaccard Index (with the score itself).
        From https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python.
    """   
    for sentence in ref_word_sentences:
        sentence = [ word.lower() for word in sentence ]
        scores.append(jaccard_similarity(ms_sentence, sentence))
                                 
    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[0]
    return top_scoring_sentence


def jaccard_similarity(x, y):
  """ Takes 2 lists of string (sentences) and
      returns the jaccard similarity between two lists (float).
  """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality / float(union_cardinality)
