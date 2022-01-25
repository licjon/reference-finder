import spacy
from jaccard_similarity import jaccard_similarity
from euclidean_distance import euclidean_distance
from nltk.tokenize import sent_tokenize, word_tokenize
from PyPDF2 import PdfFileReader

def join_punctuation(seq, characters='.,;?!'):
    characters = set(characters)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current


def get_jaccard_top_score(sentence, ref):
    sentence_lcase = [ word.lower() for word in sentence ]
    scores = []
    ref = " ".join(ref)
    ref_sentences = [word_tokenize(word.lower()) for word in sent_tokenize(ref)]
    sentence_list = []

    for sentence in ref_sentences:
        # sentence = [ word for word in sentence ]
        sentence_list.append(" ".join(sentence))
        scores.append(jaccard_similarity(sentence_lcase, sentence))
                                 
    top_scoring_sentence = sorted(zip(scores, sentence_list), reverse=True)[0]
    return top_scoring_sentence

def get_top_euclidean_distance(ms_sentence, ref):
    """ Get Euclidean distance and the top sentence matched using that score. """
    nlp = spacy.load('en_core_web_md')
    # sentence_lcase = [ word.lower() for word in sentence ]
    # sentence_string = " ".join(sentence_lcase)
    sentence_vector = nlp(" ".join(ms_sentence)).vector
    scores = []
    ref = " ".join(join_punctuation(ref))
    ref_sentences = sent_tokenize(ref)
    # ref_sentences_vector = list(nlp.pipe(ref_sentences))
    # print(type(sentence_vector))
    # print(ref_sentences_vector)
    # sentence_list = []

    for sentence in ref_sentences:
        scores.append(euclidean_distance(sentence_vector, nlp(sentence).vector))
                                 
    top_scoring_sentence = sorted(zip(scores, ref_sentences), reverse=True)[0]
    return top_scoring_sentence
