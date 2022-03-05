import json

import config

from PyPDF2 import PdfFileReader
from nltk.tokenize import sent_tokenize, word_tokenize
from pathlib import Path
from pdfminer.high_level import extract_text


class Reference:

    def __init__(self, file):
        # Speeds up program and saves memory
        __slots__ = ["name", "pdfobject",
                     "string", "sentences", "word_sentences",
                     "words", "words_sans_percent"]

        self.name = Path(file).stem
        self.pdfobject = PdfFileReader(file)

        self.string = ''
        for page in self.pdfobject.pages:
            page = page.extractText()
            self.string += ''.join(page).replace('\n', ' ')

        # List of string, each string a sentence.
        self.sentences = sent_tokenize(self.string)

        # Generator of sentences (list of words).
        self.word_sentences = (word_tokenize(word) for word in self.sentences)

        # A list of str, each item a word in the pdf.
        self.words = word_tokenize(self.string)

        # Same thing but without % to match text files.
        self.words_sans_percent = (word.strip('%') for word in self.words)

        self.embeddings = (
            config.nlp(sentence).vector for sentence in self.sentences)


class ReferenceMiner:

    def __init__(self, file):
        __slots__ = ["name",
                     "string", "sentences",
                     "word_sentences", "words",
                     "words_sans_percent"]

        file_name = Path(file)
        self.name = file_name.stem

        # Extract text with pdfminer.
        self.string = extract_text(file_name)
        self.sentences = sent_tokenize(self.string.replace('\n', ' '))
        self.word_sentences = (
            word_tokenize(word) for word in self.sentences)
        self.words = word_tokenize(self.string)
        self.words_sans_percent = (word.strip('%') for word in self.words)
        self.embeddings = (
            config.nlp(sentence).vector for sentence in self.sentences)


class ReferenceJson:

    def __init__(self, file):
        __slots__ = ["name", "sentences",
                     "word_sentences", "words",
                     "words_sans_percent"]

        self.name = file["name"]
        self.sentences = file["sentences"]
        self.word_sentences = (word_tokenize(word.replace('\n', ' ')) for word in self.sentences)
        self.words = file["words"]
        self.words_sans_percent = (word.strip('%') for word in self.words)
        self.embeddings = (
            config.nlp(sentence).vector for sentence in self.sentences)
