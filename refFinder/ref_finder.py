"""Finds supporting references for manuscript."""
import multiprocessing as mp
# from tqdm import tqdm # For progress bar (not needed w/ mp)
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
        with open(manuscript, 'r') as manuscript:
            manuscript_string = manuscript.read().replace("\n", " ")

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

        # Create the same number of processes as there are CPUs
        num_processes = mp.cpu_count()

        # Global is used to prevent local object pickling error
        global wrapper

        # Write each manuscript sentence and call find_refs with each sentence.
        # Use a pool instead of iterating through each PDF.
        for sentence in manuscript_sentences:
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)
            def wrapper(file):
                return find_refs(sentence, file)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, files)

    except IOError:
        print("Could not read from file")
        exit(1)


def find_refs(sentence, ref_file):
    """Count occurences in reference file of intersection of words in 2 files."""
    try:
        # Read pdf file
        ref = PdfFileReader(ref_file)
        ref_pages = []

        # Extract pdf and split into words
        # (list of list is a page (list) of a list of string)
        for page in ref.pages:
            ref_pages.append(page.extractText().split())

        # Flattens list of page of words to list of words
        ref_words = [word for page in ref_pages for word in page]

        # Creates list of intersection of words in the 2 lists
        intersection_words = [
            word for word in sentence if (word in ref_words)
            and (word.lower() not in set(stopwords.words('english')))]

        # Create list of intersecting numbers
        manuscript_nums = []
        for grapheme in sentence:
            try:
                if float(grapheme):
                    manuscript_nums.append(grapheme)
            except ValueError:
                continue

        intersection_nums = [num for num in manuscript_nums if (num in ref_words)]

        # Dictionary of frequency of each intersected word,
        # discarding common words
        fd = FreqDist(word for word in ref_words if word in intersection_words)

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
