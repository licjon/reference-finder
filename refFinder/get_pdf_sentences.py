import config
from cos_similarity import cos_similarity
from jaccard_similarity import jaccard_similarity
from euclidean_distance import euclidean_distance
# from nltk import edit_distance

def get_jaccard_top_score(ms_sentence, ref_sentences, ref_word_sentences):
    scores = []

    for sentence in ref_word_sentences:
        sentence = [ word.lower() for word in sentence ]
        scores.append(jaccard_similarity(ms_sentence, sentence))
                                 
    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[:3]
    return top_scoring_sentence


def get_top_euclidean_distance(ms_embeddings, ref_sentences):
    """ Get Euclidean distance and the top sentence matched using that score. """
    scores = []

    for sentence in ref_sentences:
        scores.append(euclidean_distance(ms_embeddings, config.nlp(sentence).vector))
                                 
    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[:3]
    return top_scoring_sentence

def get_top_cos_similarity(ms_embeddings, ref_sentences):
    """ TODO: refactor into 1 function with the metric fun passed as argument? """
    scores = []

    for sentence in ref_sentences:
        scores.append(cos_similarity(ms_embeddings, config.nlp(sentence).vector))

    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[:3]
    return top_scoring_sentence


""" def get_top_levenshtein_distance(ms_sentence, ref_sentences):
    scores = []

    for sentence in ref_sentences:
        scores.append(edit_distance(ms_sentence, sentence))
    
    top_scoring_sentence = sorted(zip(scores, ref_sentences))[:3]
    return top_scoring_sentence
"""

        
