import json
import multiprocessing as mp

from tqdm import tqdm

from get_refs import get_refs

def init_comparison_db(manuscript, no_save, no_db):
    """ Send dictionaires in json to get_refs. """ 
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

        with open('references.json', 'r') as references:
            refs_data = references.read()

        refs_list = json.loads(refs_data)

        # Global is used to prevent local object pickling error
        global wrapper

        # Write each manuscript sentence to output.txt and call get_refs with each sentence.
        # tqdm times the iterations.
        for sentence in tqdm(manuscript_sentences):
            ms_embeddings = next(manuscript_embeddings) 
            with open('output.txt', 'a') as output:
                lines = ['\n', "\n", ' '.join(sentence), "\n"]
                output.writelines(lines)

        # Use a thread pool to speed up the reading of json.
            def wrapper(ref):
                return get_refs(sentence, ref, ms_embeddings, True, no_save, no_db)
            with mp.Pool(processes=num_processes) as pool:
                pool.map(wrapper, refs_list)

    except IOError:
        print("init_comparison: Could not read/write file")
        pass
