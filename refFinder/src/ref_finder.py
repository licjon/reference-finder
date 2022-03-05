"""Find supporting references for manuscript.
   Arguments: file (txt or docx) and 3 optional arguments:
   path (only optional after running once without --nosave flag)
   --nosave
   --nodb
"""

import argparse
import glob
import json
import os

from pathlib import Path

from manuscript_class import Manuscript
from mydocument_class import MyDocument
from reference_class import Reference, ReferenceMiner
from init_comparison import init_comparison


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
        # Create a list of paths.
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
        print("Please report issue to https://github.com/licjon/reference-finder/issues")


if __name__ == "__main__":
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
