from jaccard_similarity import jaccard_similarity
from nltk.tokenize import sent_tokenize, word_tokenize
from PyPDF2 import PdfFileReader

def get_pdf_sentence(sentence, ref):
    sentence_lcase = [ word.lower() for word in sentence ]
    scores = []
    ref = " ".join(ref)
    ref_sentences = [word_tokenize(word) for word in sent_tokenize(ref)]
    sentence_list = []

    for sentence in ref_sentences:
        sentence = [ word.lower() for word in sentence ]
        sentence_list.append(sentence)
        scores.append(jaccard_similarity(sentence_lcase, sentence))
                                 
    top_scoring_sentence = sorted(zip(scores, sentence_list), reverse=True)[0]
    return top_scoring_sentence
