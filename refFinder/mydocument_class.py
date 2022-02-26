import docx
from nltk.tokenize import sent_tokenize, word_tokenize
import config


class MyDocument:
     
     # doc is "dmd_manuscript.docx" for example
     def __init__(self, doc):
          
          __slots__ = ['embeddings']

          # type: <class 'docx.document.Document'>
          self.doc = docx.Document(doc)

          # type: list of <class 'docx.text.paragraph.Paragraph'>
          self.all_paras = self.doc.paragraphs
          
          # type: list of string
          self.para_list = [para.text for para in self.all_paras]

          # type: list of list of string
          self.sentences = self.__get_sentence_list()

          # Generator of sentences, each sentence a list of words
          self.words = (
            word_tokenize(word) for word in self.sentences )

          self.embeddings = (
               config.nlp(sentence).vector for sentence in self.sentences )

     def __get_sentence_list(self):
          sent_list = []
          sentence_list = []
          for para in self.para_list:
               if len(para) > 0:
                    sent_list.append(sent_tokenize(para))

          for sentence in sent_list:
               if len(sentence) < 1:
                    sent_list.remove(sentence)

          for para in sent_list:
               for sentence in para:
                   sentence_list.append(sentence) 

          return sentence_list
                    
