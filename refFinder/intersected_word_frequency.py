from nltk.probability import FreqDist
from nltk.corpus import stopwords


MY_STOPWORDS = stopwords.words('english')
newStopWords = ['+', '*', '.', '=', ',', '(', ')', '[', ']', 'p']
MY_STOPWORDS.extend(newStopWords)

def intersected_word_frequency(sentence, ref_words):
    """Return dictionary of frequency of interesected word in reference as key and word as value."""
    
    # Creates list of intersection of words in the 2 lists
    intersection_words = [
        word for word in sentence if (word in ref_words)
        and (word.lower() not in set(MY_STOPWORDS))]

    # Dictionary of frequency of each intersected word, discarding common words
    fd = FreqDist(word for word in ref_words if word in intersection_words)

    return fd
