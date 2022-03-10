from PyPDF2 import PdfFileReader
from pdfminer.high_level import extract_text

from reference_class import Reference, ReferenceMiner

def create_pdf_class(file):
    manuscript_pdf = Reference(file)
    sentences = manuscript_pdf.sentences
    # Check if PyPDF read the pdf properly.
    if not sentences or len(manuscript_pdf.words[0]) > 15:
        # If not, try again with pdfminer
        manuscript_pdf = ReferenceMiner(file)
        sentences = manuscript_pdf.sentences
        # If that doesn't work, give up.
        if not sentences or len(manuscript_pdf.words[0]) > 15:
            print("Manuscript pdf cannot be read. Program aborted.")
            exit(1)
            
    return manuscript_pdf
