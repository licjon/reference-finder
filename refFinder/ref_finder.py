"""Finds supporting references for manuscript."""
# My modules
from store_ref import store_ref
from check_db import check_db
from mydocument_class import MyDocument
from reference_class import Reference, Reference_miner, Reference_json
from manuscript_class import Manuscript
from write_results import write_results
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from get_pdf_sentences import get_jaccard_top_score, get_top_euclidean_distance, get_top_cos_similarity#, get_top_levenshtein_distance
from jaccard_similarity import jaccard_similarity
# Libraries
import json
from pathlib import Path
import _pickle as pickle
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
        # word embeddings
        manuscript_embeddings = manuscript.embeddings

        # Global is used to prevent local object pickling error
        global wrapper

        # Write each manuscript sentence to output.txt and call vet_refs with each sentence.
        # tqdm times the iterations.
        for sentence in tqdm(manuscript_sentences):
            ms_embeddings = next(manuscript_embeddings) 
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)

        # Use a thread pool to speed up the reading of PDFs.
            def wrapper(file):
                return vet_refs(sentence, ms_embeddings, file)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, files)

    except IOError:
        print("init_comparison: Could not read/write file")
        pass


def vet_refs(sentence, ms_embeddings, ref_file):
    """Pick the best method of reading the pdf or move to next ref if unreadable."""
    try:
        # check if reference is stored, return boolean
        # ref_file is str
        is_stored = check_db(ref_file)
        # print(str(type(is_stored)))

        if is_stored != None:
            # print("get_refs w/ json")
            get_refs(sentence, is_stored, ms_embeddings, is_stored)
            return 0
        else:
            ref = Reference(ref_file)

            ref_sentences = ref.sentences

            # Check if PyPDF read the pdf properly. 
            if not ref_sentences or len(ref.words[0]) > 15:
                # If not, try again with pdfminer
                ref = Reference_miner(ref_file)
                ref_sentences = ref.sentences
                # If that doesn't work, give up
                if not ref_sentences or len(ref.words[0]) > 15:
                    with open('output.txt', 'a') as output:
                        output.write('{} cannot be read \n'.format(ref.name))
                        return 0
                # If it works, call get_refs w/ Reference_miner class
                else: get_refs(sentence, ref, ms_embeddings, is_stored)
            else:
                get_refs(sentence, ref, ms_embeddings, is_stored)

    except IOError:
        print("find_refs: could not read/write file.")
        exit(1)


def get_refs(sentence, ref, ms_embeddings, is_stored):
    """Collect different metrics and send them to be written in output file."""
    # will check is_stored and if true use json

    if is_stored != None:
        ref = Reference_json(ref) 

    ref_sentences = ref.sentences

    # Get top scoring sentence with the Jaccard Score
    top_scoring_sentence = get_jaccard_top_score(sentence, ref_sentences, ref.word_sentences)

    euclidean_distance = get_top_euclidean_distance(ms_embeddings, ref_sentences)

    cos_similarity = get_top_cos_similarity(ms_embeddings, ref_sentences)
        
    # levenshtein_distance = get_top_levenshtein_distance(sentence, ref_sentences)
        
    # Get list of numbers shared by manuscript and reference
    intersection_nums = intersection_numbers(sentence, ref.words_sans_percent)
        
    fd = intersected_word_frequency(sentence, ref.words)
        
    total_matches = sum(fd.values())

    # Number of words matched
    length_fd = len(fd)

    write_results(
        ref.name, top_scoring_sentence, euclidean_distance, cos_similarity, intersection_nums, total_matches, length_fd, fd)

    if is_stored == None:
        # print(str(is_stored))
        # print("json written")
        store_ref(ref)
        return 0
    else:
        return 0


def main():
    try:
        # Arguments. Run "python ref_finder.py file.txt ~/path/to/pdf/directory"
        _, manuscript, refs_path = argv
        
        # Instantiate Manuscript class
        base, ext = os.path.splitext(manuscript)
        if ext == ".txt":
            manuscript = Manuscript(manuscript)
        else:
            manuscript = MyDocument(manuscript)

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
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
