"""Finds supporting references for manuscript."""
# My modules
from reference_class import Reference
from manuscript_class import Manuscript
from write_results import write_results
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from get_pdf_sentences import get_jaccard_top_score, get_top_euclidean_distance, get_top_cos_similarity
from jaccard_similarity import jaccard_similarity
# Libraries
import multiprocessing as mp
from tqdm import tqdm
from sys import argv
import os
import glob


def init_comparison(manuscript, files):
    """Initialize comparison."""
    try:
        # Create the same number of processes as there are CPUs
        num_processes = mp.cpu_count()

        # list of list of string
        manuscript_sentences = manuscript.words
        manuscript_embeddings = manuscript.embeddings

        # Global is used to prevent local object pickling error
        global wrapper

        # Write each manuscript sentence to output.txt and call find_refs with each sentence.
        # tqdm times the iterations.
        for i, sentence in tqdm(enumerate(manuscript_sentences)):
            ms_embeddings = manuscript_embeddings[i] 
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)

        # Use a thread pool to speed up the reading of PDFs.
            def wrapper(file):
                return find_refs(sentence, ms_embeddings, file)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, files)

    except IOError:
        print("init_comparison: Could not read/write file")
        exit(1)


def find_refs(sentence, ms_embeddings, ref_file):
    """Find intersecting words and numbers."""
    try:
        ref = Reference(ref_file)

        # Get top scoring sentence with the Jaccard Score
        top_scoring_sentence = get_jaccard_top_score(sentence, ref.sentences, ref.word_sentences)

        euclidean_distance = get_top_euclidean_distance(ms_embeddings, ref.sentences)

        cos_similarity = get_top_cos_similarity(ms_embeddings, ref.sentences)
        
        # Get list of numbers shared by manuscript and reference
        intersection_nums = intersection_numbers(sentence, ref.words_sans_percent)
        
        fd = intersected_word_frequency(sentence, ref.words)
        
        total_matches = sum(fd.values())

        # Number of words matched
        length_fd = len(fd)

        write_results(
            ref.name, intersection_nums, total_matches, length_fd, fd, top_scoring_sentence, euclidean_distance, cos_similarity)

    except IOError:
        print("find_refs: Could not read from file")
        exit(1)


def main():
    try:
        # Arguments. Run "python ref_finder.py file.txt ~/path/to/pdf/directory"
        _, manuscript, refs_path = argv
        
        # Instantiate Manuscript class
        manuscript = Manuscript(manuscript)

        # Creates a list of paths
        files = glob.glob(os.path.join(refs_path, '*.pdf'))
        
        # Start writing file.
        with open('output.txt', 'w') as output:
            output.write(
                "***OUTPUT OF COMPARISON OF MANUSCRIPT AND REFERENCE(S)*** \n \n")
            
        init_comparison(manuscript, files)
            
    except IOError:
        print("main: could not read/write file.")
        exit(1)

if __name__ == "__main__":
    main()
