import json

from pathos.pools import ProcessPool
from tqdm import tqdm

from check_db import check_db
from get_refs import get_refs
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

    # Write each manuscript sentence to output.txt.
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
            # Same as above but with json and calls get_refs.
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
        # Use json
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
        # Use Reference class
        elif no_db:
            get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
        else:
            get_refs(sentence, ref, ms_embeddings, False, no_save, no_db)

