"""Finds supporting references for manuscript."""

import argparse
import glob
import json
import os

from pathlib import Path
from pathos.pools import ProcessPool
from tqdm import tqdm

from check_db import check_db
from get_refs import get_refs
from manuscript_class import Manuscript
from mydocument_class import MyDocument
from reference_class import Reference, ReferenceMiner


def init_comparison(manuscript, no_save, no_db, files = None):
    """Initialize comparison."""
    # Start writing file.
    with open("output.txt", 'w') as output:
        output.write(
            "***OUTPUT OF COMPARISON OF MANUSCRIPT AND REFERENCE(S)*** \n \n")

    # list of list of string
    manuscript_sentences = manuscript.words
    # word embeddings
    manuscript_embeddings = manuscript.embeddings

    # Write each manuscript sentence to output.txt
    # and call vet_refs with each sentence.
    # tqdm times the iterations.
    for sentence in tqdm(manuscript_sentences):
        ms_embeddings = next(manuscript_embeddings)
        with open("output.txt", 'a') as output:
            lines = ['\n', '\n', ' '.join(sentence), '\n']
            output.writelines(lines)
        if files is not None:
            # Use a thread pool to speed up the reading of PDFs.
            def wrapper(file):
                return vet_refs(sentence, ms_embeddings, file, no_save,
                                no_db)
            with ProcessPool() as pool:
                pool.map(wrapper, files)
        else:
            # Use a thread pool to speed up the reading of json.
            with open("references.json", 'r') as references:
                refs_data = references.read()
            refs_list = json.loads(refs_data)
            def wrapper(ref):
                return get_refs(sentence, ref, ms_embeddings, True,
                                no_save, no_db)
            with ProcessPool() as pool:
                pool.map(wrapper, refs_list)


def vet_refs(sentence, ms_embeddings, ref_file, no_save, no_db):
    """Pick the best method of reading the pdf or
       move to next ref if unreadable."""
        # return dictionary if reference is stored, else return None
    is_stored = check_db(ref_file) # ref_file is str

    if is_stored and not no_db:
        get_refs(sentence, is_stored, ms_embeddings, True, no_save, no_db)
    else:
        ref = Reference(ref_file)
        ref_sentences = ref.sentences

        # Check if PyPDF read the pdf properly.
        if not ref_sentences or len(ref.words[0]) > 15:
            # If not, try again with pdfminer
            ref = ReferenceMiner(ref_file)
            ref_sentences = ref.sentences
            # If that doesn't work, give up and move on.
            if not ref_sentences or len(ref.words[0]) > 15:
                with open("output.txt", 'a') as output:
                    output.write("{} cannot be read \n".format(ref.name))
            # If it works, call get_refs w/ ReferenceMiner class.
            elif no_db:
                get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
            else: get_refs(sentence, ref, ms_embeddings, False, no_save,
                           no_db)
        elif no_db:
            get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
        else:
            get_refs(sentence, ref, ms_embeddings, False, no_save, no_db)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manuscript",
        help="Text or docx file that will be compared to the PDFs.",
        type=str
    )
    parser.add_argument(
        "--nosave",
        help="Do not save references to database.",
        action="store_true"
    )
    parser.add_argument(
        "--nodb",
        help="Do not use references in database.",
        action="store_true"
    )
    parser.add_argument(
        "refs_path",
        nargs='?', help="Path to directory of PDFs.",
        type=str, default=None
    )

    args = parser.parse_args()
    manuscript = args.manuscript
    refs_path = args.refs_path
    no_save = args.nosave
    no_db = args.nodb

    # Check if json is empty
    with open("references.json", 'r') as references:
        refs_data = references.read()
    refs_dict = json.loads(refs_data)
    if len(refs_dict) == 0:
        refs_in_db = False
    else:
        refs_in_db = True

    # Instantiate Manuscript class
    _, ext = os.path.splitext(manuscript)
    if ext == ".txt":
        manuscript = Manuscript(manuscript)
    else:
        manuscript = MyDocument(manuscript)

    if refs_path is not None:
        # Creates a list of paths
        files = glob.glob(os.path.join(refs_path, "*.pdf"))

    # With just the file, using stored refs: file
    if not refs_path and refs_in_db and not no_db and not no_db:
        init_comparison(manuscript, no_save, no_db)
    # With new refs (that are stored if not in database) that may
    # or may not be in the database: file path [--nosave --nodb]
    elif refs_path is not None:
        init_comparison(manuscript, no_save, no_db, files)
    elif not refs_path and no_db:
        print("Error: No file path was provided.")
    elif not refs_path and not refs_in_db:
        print("Error: Database is empty. Please include path to file(s).")
    else:
        print("Please report issue to [github url]")


if __name__ == "__main__":
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
