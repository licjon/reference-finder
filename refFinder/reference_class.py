from nltk.tokenize import sent_tokenize, word_tokenize
import re
import config
from PyPDF2 import PdfFileReader

  
class Reference:

    def __init__(self, file):

        path_list = re.split(r'\/+', file)

        self.name = path_list[-1] 
        self.pdfobject = PdfFileReader(file)

        # The entire contents of the pdf in a string
        self.string = ''

        for page in self.pdfobject.pages:
            page = page.extractText()
            self.string += "".join(page).replace('\n', '')
        
        # List of string, each string a sentence
        self.sentences = sent_tokenize(self.string)
        
        # Embeddings of sentences
        self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

        # List of sentences of list of words
        self.word_sentences = [ word_tokenize(word) for word in sent_tokenize(self.string) ]

        # A list of str, each item a word in the pdf
        self.words = word_tokenize(self.string) 

        # Same thing but without % to match text files
        self.words_sans_percent = [ word.strip("%") for word in self.words ]
