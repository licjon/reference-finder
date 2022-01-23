from nltk.tokenize import sent_tokenize, word_tokenize

def read_manuscript(manuscript):
    """Read text file and return list of list of string."""
    try:
        # Open text file and convert to string
        with open(manuscript, 'r') as manuscript:
            manuscript_string = manuscript.read().replace("\n", " ")

        # List of list of strings: Each sentence has list of words.
        manuscript_sentences = [
            word_tokenize(word) for word in sent_tokenize(manuscript_string)]

        return manuscript_sentences

    except IOError:
        print("read_manuscript: Could not read from file")
        exit(1)
