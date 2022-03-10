from nltk.tokenize import sent_tokenize, word_tokenize

import config


class Manuscript:

    def __init__(self, file):
        __slots__ = ["string", "sentences", "words", "embeddings"]

        self.string = self.__read_file(file)

        # List of string, each string a sentence.
        self.sentences = sent_tokenize(self.string)

        # Generator of sentences, each sentence is a list of words.
        self.words_ms = (
            word_tokenize(word) for word in self.sentences)

        # Generator of embeddings of the words for each sentence.
        self.embeddings = (
            config.nlp(sentence).vector for sentence in self.sentences)

    def __read_file(self, file):
        """ Text file as string. """
        with open(file, 'r') as file:
            manuscript_string = file.read().replace('\n', ' ')
            
        return manuscript_string
