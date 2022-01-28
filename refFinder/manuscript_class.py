from nltk.tokenize import sent_tokenize, word_tokenize
import config


class Manuscript:

    def __init__(self, file):
        # nlp = spacy.load('en_core_web_md')
        self.string = self.__read_file(file)
        self.sentences = sent_tokenize(self.string)
        # List of sentences, each sentence is a list of words 
        self.words = [
            word_tokenize(word) for word in sent_tokenize(self.string) ]
        self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

    def __read_file(self, file):
        """ Text file as string. """
        try:
            with open(file, 'r') as file:
                manuscript_string = file.read().replace("\n", " ")

            return manuscript_string
        
        except IOError:
            print("manuscript class: Could not read from file")
            exit(1)


