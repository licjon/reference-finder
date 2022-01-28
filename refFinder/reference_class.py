from nltk.tokenize import sent_tokenize, word_tokenize
import re
import config
from PyPDF2 import PdfFileReader


class Reference:

    def __init__(self, file):

        path_list = re.split(r'\/+', file)
        self.name = path_list[-1] 
        self.pdfobject = PdfFileReader(file)

        count = self.pdfobject.numPages
        self.pages = ''
        for i in range(count):
            page = self.pdfobject.getPage(i)
            self.pages += page.extractText()

        # I have 2 self.pages because the one below is a list and works for word and number matching 
        # List of str, each item a string of pdf page's contents
        self.pages_list = [
            page.extractText().split() for page in self.pdfobject.pages ]

        self.string = "".join(self.pages).replace('\n', '')
        self.sentences = sent_tokenize(self.string)
        
        # Embeddings of sentences
        self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

        # List of sentences of list of words
        self.word_sentences = [ word_tokenize(word) for word in sent_tokenize(self.string) ]

        # A list of str, each item a word in the pdf
        self.words = [ word.lower() for page in self.pages_list for word in page ]

        # Same thing but without % to match text files
        self.words_sans_percent = [
            word.strip("%") for page in self.pages_list for word in page ]
