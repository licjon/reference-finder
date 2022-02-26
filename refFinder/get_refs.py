import json

from get_pdf_sentences import get_jaccard_top_score, get_top_euclidean_distance, get_top_cos_similarity#, get_top_levenshtein_distance
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from manuscript_class import Manuscript
from mydocument_class import MyDocument
from reference_class import Reference, Reference_miner, Reference_json
from store_ref import store_ref
from write_results import write_results


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
