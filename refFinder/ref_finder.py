"""Finds supporting references for manuscript."""

import argparse
import glob
import json
import multiprocessing as mp
import os

from pathlib import Path
from tqdm import tqdm

from check_db import check_db
from get_pdf_sentences import get_jaccard_top_score, get_top_euclidean_distance, get_top_cos_similarity#, get_top_levenshtein_distance
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from jaccard_similarity import jaccard_similarity
from manuscript_class import Manuscript
from mydocument_class import MyDocument
from reference_class import Reference, Reference_miner, Reference_json
from store_ref import store_ref
from write_results import write_results

def init_comparison(manuscript, files, no_save, no_db):
    """Initialize comparison."""
    try:
        # Start writing file.
        with open('output.txt', 'w') as output:
            output.write(
                "***OUTPUT OF COMPARISON OF MANUSCRIPT AND REFERENCE(S)*** \n \n")

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
                return vet_refs(sentence, ms_embeddings, file, no_save, no_db)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, files)

    except IOError:
        print("init_comparison: Could not read/write file")
        pass


def vet_refs(sentence, ms_embeddings, ref_file, no_save, no_db):
    """Pick the best method of reading the pdf or move to next ref if unreadable."""
    try:
        # return dictionary if reference is stored, else return None
        is_stored = check_db(ref_file) # ref_file is str

        if is_stored and not no_db:
            # print("get_refs w/ json")
            get_refs(sentence, is_stored, ms_embeddings, True, no_save, no_db)
        else:
            ref = Reference(ref_file)

            # print("not json")
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
                elif no_db:
                    get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
                else: get_refs(sentence, ref, ms_embeddings, False, no_save, no_db)
            elif no_db:
                get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
            else:
                get_refs(sentence, ref, ms_embeddings, False, no_save, no_db)

    except IOError:
        print("find_refs: could not read/write file.")
        exit(1)


def get_refs(sentence, ref, ms_embeddings, is_stored, no_save, no_db):
    """Collect different metrics and send them to be written in output file."""

    if is_stored and not no_db:
        # print("json")
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

    if not is_stored and not no_save:
        # print(str(is_stored))
        # print("json written")
        store_ref(ref)
        return 0
    else:
        return 0


def main():
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument("manuscript", help="Text or docx file that will be compared to the PDFs.", type=str)

        parser.add_argument("--nosave", help="Do not save references to database.", action="store_true")

        parser.add_argument("--nodb", help="Do not use references in database.", action="store_true")

        parser.add_argument("refs_path", nargs='?', help="Path to directory of PDFs.", type=str, default=None)

        args = parser.parse_args()

        manuscript = args.manuscript
        refs_path = args.refs_path

        no_save = args.nosave
        no_db = args.nodb

        # Check if json is empty
        with open('references.json', 'r') as references:
            refs_data = references.read()

        refs_dict = json.loads(refs_data)

        if len(refs_dict) == 0:
            refs_in_db = False
        else:
            refs_in_db = True
 
        # If run without a path the first time, there should be an error
        if not refs_path and not refs_in_db and not no_save:
            print("Error: need file path")
            exit(1)

        # Instantiate Manuscript class
        _, ext = os.path.splitext(manuscript)
        if ext == ".txt":
            manuscript = Manuscript(manuscript)
        else:
            manuscript = MyDocument(manuscript)

        if refs_path:
            # Creates a list of paths
            files = glob.glob(os.path.join(refs_path, '*.pdf'))
        
        # With just the file, using stored refs: file
        if not refs_path and refs_in_db and not no_db and not no_db:
            print("Using database with no new refs. Need to make new function that doesn't take files or make files parameter optional")
        # With new refs (that are stored if not in database) that may or may not be in the database: file path
        elif refs_path:
            print("Using new refs. Maybe there are refs in the database. Maybe save.")
            init_comparison(manuscript, files, no_save, no_db)
        # New refs but no save (can use stored refs if new refs alreadys tored [optional if not difficult])
        elif refs_path and no_save and not no_db:
            print("Use new refs but don't save. Need to make it so it doesn't save but can use stored ref if already saved.") 
        # Use new refs, don't use stored refs even if they are stored and don't save. This would be used if using a few refs and want quick results.
        elif refs_path and not no_save and no_db:
            print("Use new refs, save them, do not use database.")
        elif refs_path and no_save and no_db:
            print("New refs, no database, and no save")
        elif not refs_path and no_db and no_save:
            print("Error: No file path was provided.")
        else:
            print("Please report issue to [github url]")
            exit(1)
                    
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
