from PyPDF2 import PdfFileReader
from nltk.tokenize import sent_tokenize, word_tokenize

def match_sentence(sentence, path):
    """ Returns true if sentence can be found in file. """

    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)

        pdf_string = ''

        for page in pdf.pages:
            page = page.extractText()
            pdf_string += "".join(page).replace('\n', '')
        
            # Extract text with pdfminer
            # pdf_string = extract_text(Path(file))

        # List of string, each string a sentence
        sentences = sent_tokenize(pdf_string)

        for ref_sentence in sentences:
            if sentence == ref_sentence:
                return True

