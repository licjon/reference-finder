from itertools import zip_longest

from jaccard_similarity import jaccard_similarity


def get_jaccard_top_score(ms_sentence, ref_sentences, ref_word_sentences):
    scores = []
    
    for sentence in ref_word_sentences:
        sentence = [ word.lower() for word in sentence ]
        scores.append(jaccard_similarity(ms_sentence, sentence))
                                 
    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[0]
    return top_scoring_sentence
