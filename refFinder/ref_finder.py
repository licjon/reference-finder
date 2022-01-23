"""Finds supporting references for manuscript."""
# My modules
from write_results import write_results
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from get_pdf_sentences import get_pdf_sentence
from read_manuscript import read_manuscript
from jaccard_similarity import jaccard_similarity
# Libraries
import multiprocessing as mp
from tqdm import tqdm
import re
from sys import argv
from PyPDF2 import PdfFileReader
from pathlib import Path
import os
import glob


def init_comparison(manuscript_sentences, files):
    """Initialize comparison."""
    try:
        # Create the same number of processes as there are CPUs
        num_processes = mp.cpu_count()

        # Global is used to prevent local object pickling error
        global wrapper

        # Write each manuscript sentence to output.txt and call find_refs with each sentence.
        # tqdm times the iterations.
        for sentence in tqdm(manuscript_sentences):
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)

        # Use a thread pool to speed up the reading of PDFs.
            def wrapper(file):
                return find_refs(sentence, file)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, files)

    except IOError:
        print("init_comparison: Could not read from file")
        exit(1)


def find_refs(sentence, ref_file):
    """Find intersecting words and numbers."""
    try:
        # Read pdf file
        ref = PdfFileReader(ref_file)

        # Extract pdf and split into words
        # (list of list is a page (list) of a list of string)
        ref_pages = []
        for page in ref.pages:
            ref_pages.append(page.extractText().split())

        # Flattens list of page of words to list of words
        # Strip % signs because text file splits number from % but pdf doesn't
        ref_words = [word.strip("%") for page in ref_pages for word in page]

        # get top scoring sentence with the Jaccard Score
        top_scoring_sentence = get_pdf_sentence(sentence, ref_words)

        # Get list of numbers shared by manuscript and reference
        intersection_nums = intersection_numbers(sentence, ref_words)
        
        fd = intersected_word_frequency(sentence, ref_words)
        
        total_matches = sum(fd.values())

        # Number of words matched
        length_fd = len(fd)

        # Get file name
        path_list = re.split(r'\/+', ref_file)
        file_name = path_list[-1]

        write_results(
            file_name, intersection_nums, total_matches, length_fd, fd, top_scoring_sentence)

    except IOError:
        print("find_refs: Could not read from file")
        exit(1)


def main():
    """Do the main function."""
    # Arguments. Run "python ref_finder.py file.txt ~/path/to/pdf/directory"
    _, manuscript, refs_path = argv

    manuscript_sentences = read_manuscript(manuscript)

    # Creates a list of paths
    files = glob.glob(os.path.join(refs_path, '*.pdf'))

    # Start writing file.
    with open('output.txt', 'w') as output:
        output.write(
            "***OUTPUT OF COMPARISON OF MANUSCRIPT AND REFERENCE(S)*** \n \n")

    # TODO return value and assign to variable and continue calling functions in main
    init_comparison(manuscript_sentences, files)


if __name__ == "__main__":
    main()
