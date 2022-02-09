from nltk.tokenize import sent_tokenize, word_tokenize
# import config
from PyPDF2 import PdfFileReader
from pathlib import Path
from pdfminer.high_level import extract_text
import json

class Reference:

    def __init__(self, file):
        
        # Speeds up program and saves memory
        __slots__ = ['name',
                     'pdfobject',
                     'string', 'sentences', 'word_sentences', 'words', 'words_sans_percent']

        # string
        self.name = Path(file).stem

        self.pdfobject = PdfFileReader(file)

        # The entire contents of the pdf in a string
        self.string = ''

        for page in self.pdfobject.pages:
            page = page.extractText()
            self.string += "".join(page).replace('\n', '')
        
        # Extract text with pdfminer
        # self.string = extract_text(Path(file))

        # List of string, each string a sentence
        self.sentences = sent_tokenize(self.string)

        # Embeddings of sentences
        # self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

        # List of sentences of list of words
        self.word_sentences = ( word_tokenize(word) for word in sent_tokenize(self.string) )

        # A list of str, each item a word in the pdf
        self.words = word_tokenize(self.string) 

        # Same thing but without % to match text files
        self.words_sans_percent = ( word.strip("%") for word in self.words )


class Reference_miner:
    
    def __init__(self, file):
        
        # Speeds up program and saves memory
        __slots__ = ['name',
                     'string', 'sentences', 'word_sentences', 'words', 'words_sans_percent']

        # string
        file_name = Path(file)
        self.name = file_name.stem

        # The entire contents of the pdf in a string
        # Extract text with pdfminer
        self.string = extract_text(file_name)

        # List of string, each string a sentence
        self.sentences = sent_tokenize(self.string.replace('\n', ''))

        # Embeddings of sentences
        # self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

        # Generator of sentences of list of words
        self.word_sentences = ( word_tokenize(word) for word in sent_tokenize(self.string) )

        # A list of str, each item a word in the pdf
        self.words = word_tokenize(self.string) 

        # Same thing but generator without % to match text files
        self.words_sans_percent = ( word.strip("%") for word in self.words )


class Reference_miner:
    
    def __init__(self, file):
        
        # Speeds up program and saves memory
        __slots__ = ['name',
                     'string', 'sentences', 'word_sentences', 'words', 'words_sans_percent']

        # string
        file_name = Path(file)
        self.name = file_name.stem

        # The entire contents of the pdf in a string
        # Extract text with pdfminer
        self.string = extract_text(file_name)

        # List of string, each string a sentence
        self.sentences = sent_tokenize(self.string.replace('\n', ''))

        # Embeddings of sentences
        # self.embeddings = [ config.nlp(sentence).vector for sentence in self.sentences ]

        # Generator of sentences of list of words
        self.word_sentences = ( word_tokenize(word) for word in sent_tokenize(self.string) )

        # A list of str, each item a word in the pdf
        self.words = word_tokenize(self.string) 

        # Same thing but generator without % to match text files
        self.words_sans_percent = ( word.strip("%") for word in self.words )


class Reference_json:
    
    def __init__(self, file):
        
        # Speeds up program and saves memory
        __slots__ = ['name',
                     'sentences', 'word_sentences', 'words', 'words_sans_percent']

        # name from json string

        self.name = file["name"]

        # List of string, each string a sentence
        self.sentences = file["sentences"]

        # Generator of sentences of list of words
        self.word_sentences = ( word_tokenize(word) for word in self.sentences )

        # A list of str, each item a word in the pdf
        self.words = file["words"] 

        # Same thing but generator without % to match text files
        self.words_sans_percent = ( word.strip("%") for word in self.words )
