from nltk.tokenize import sent_tokenize, word_tokenize
import config


class Manuscript:

    def __init__(self, file):

        # Uncomment slots if memory becomes an issue. Slows down program.
        # __slots__ = ['string', 'sentences', 'words', 'embeddings']

        self.string = self.__read_file(file)

        # List of string, each string a sentence
        self.sentences = sent_tokenize(self.string)
        
        # List of sentences, each sentence is a list of words 
        self.words = (
            word_tokenize(word) for word in self.sentences )

        # Generator of embeddings of the words for each sentence.
        self.embeddings = ( config.nlp(sentence).vector for sentence in self.sentences )

    def __read_file(self, file):
        """ Text file as string. """
        try:
            with open(file, 'r') as file:
                manuscript_string = file.read().replace("\n", " ")

            return manuscript_string
        
        except IOError:
            print("manuscript class: Could not read from file")
            exit(1)


