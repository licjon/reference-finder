"""Finds supporting references for manuscript."""
from tqdm import tqdm
import re
from sys import argv
# from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from PyPDF2 import PdfFileReader
# from pathlib import Path
import os
import glob


def read_manuscript(manuscript):
    try:
        # Opens text file and convert to string
        with open(manuscript, 'r') as ff:  # , open(secondfile, 'r') as sf:
            manuscript_string = ff.read().replace("\n", " ")

        return manuscript_string
    except IOError:
        print("Could not read from file")
        exit(1)


def init_comparison(manuscript_string, refs_path):
    try:
        # List of list of string: Each sentence has list of words.
        manuscript_sentences = [
            word_tokenize(word) for word in sent_tokenize(manuscript_string)]

        # Creates a list of paths
        files = glob.glob(os.path.join(refs_path, '*.pdf'))

        # Start writing file.
        with open('output.txt', 'w') as output:
            output.write(
                "***OUTPUT OF COMPARISON OF MANUSCRIPT AND REFERENCE(S)*** \n \n")

        # Write each manuscript sentence and call find_refs with each sentence,
        # iterating through each PDF
        for sentence in tqdm(manuscript_sentences):
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)
            for file in files:
                find_refs(sentence, file)

    except IOError:
        print("Could not read from file")
        exit(1)


def find_refs(sentence, ref_file):
    """Count occurences in reference file of intersection of words in 2 files."""
    try:
        # Read pdf file
        sf = PdfFileReader(ref_file)
        sf_pages = []

        # Extract pdf and split into words
        # (list of list is a page (list) of a list of string)
        for page in sf.pages:
            sf_pages.append(page.extractText().split())

        # Creates list of words in pdf
        sf_words = [word for page in sf_pages for word in page]

        # Creates list of intersection of words in the 2 lists
        intersection_words = [
            word for word in sentence if (word in sf_words)
            and (word not in set(stopwords.words('english')))]

        # Create list of intersecting numbers
        ff_nums = []
        for grapheme in sentence:
            try:
                if float(grapheme):
                    ff_nums.append(grapheme)
            except ValueError:
                continue

        intersection_nums = [num for num in ff_nums if (num in sf_words)]

        # Dictionary of frequency of each intersected word,
        # discarding common words
        fd = FreqDist(word for word in sf_words if word in intersection_words)

        total_matches = sum(fd.values())

        # Number of words matched
        length_fd = len(fd)

        # Set name of file
        path_list = re.split(r'\/+', ref_file)
        file_name = path_list[-1]

        write_results(
            file_name, intersection_nums, total_matches, length_fd, fd)

    except IOError:
        print("Could not read from file")
        exit(1)


def write_results(file_name, intersection_nums, total_matches, length_fd, fd):
    try:
        # Writes fd, total_matches, length_fd to output file
        with open('output.txt', 'a') as output:
            lines = ['\n', "Reference: ", file_name, "\n",
                     "Numbers matched: ", str(intersection_nums), "\n",
                     "Total matches: ", str(total_matches), "\n",
                     "Number of words matched: ", str(length_fd), "\n",
                     "Words matched: "]
            output.writelines(lines)

        with open('output.txt', 'a') as output:
            # output.write(str(fd.most_common(20)))
            output.write(', '.join("{}: {}".format(k, v)
                                   for k, v in fd.items()))

        with open('output.txt', 'a') as output:
            output.write('\n')

    except IOError:
        print("Could not append to file")
        exit(1)


def main():
    """Do the main function."""
    # Arguments. Run "python ref_finder.py file.txt ~/path/to/pdf/directory"
    _, manuscript, refs_path = argv

    manuscript_string = read_manuscript(manuscript)

    init_comparison(manuscript_string, refs_path)


if __name__ == "__main__":
    main()
