import json

from itertools import zip_longest

from cos_similarity import cos_similarity
from euclidean_distance import euclidean_distance
from jaccard import get_jaccard_top_score
from intersected_word_frequency import intersected_word_frequency
from intersection_numbers import intersection_numbers
from manuscript_class import Manuscript
from mydocument_class import MyDocument
from reference_class import Reference, ReferenceMiner, ReferenceJson
from store_ref import store_ref
from write_results import write_results


def get_refs(sentence, ref, ms_embeddings, is_stored, no_save, no_db):
    """Collect different metrics and
       send them to be written in output file.
    """
    if is_stored and not no_db:
        ref = ReferenceJson(ref)

    ref_sentences = ref.sentences

    top_scoring_sentence = get_jaccard_top_score(sentence,
                                                 ref_sentences,
                                                 ref.word_sentences)

    # Since embeddings are generators and need to be used twice,
    # bind each embedding and call the 2 funs below w/ it
    euclidean_scores = []
    cos_scores = []
    for x in ref.sentences:
        ref_embeddings = next(ref.embeddings)
        euclidean_scores.append(euclidean_distance(ms_embeddings,
                                         ref_embeddings))
        cos_scores.append(cos_similarity(ms_embeddings,
                                         ref_embeddings))
     
    euclidean_distance_result = sorted(zip(euclidean_scores, ref_sentences), reverse=True)[0]
    cos_similarity_result = sorted(zip(cos_scores, ref_sentences), reverse=True)[0]

    # Get list of numbers shared by manuscript and reference.
    intersection_nums = intersection_numbers(sentence, ref.words_sans_percent)

    fd = intersected_word_frequency(sentence, ref.words)

    total_matches = sum(fd.values())

    # Number of words matched
    length_fd = len(fd)

    write_results(
        ref.name, top_scoring_sentence,
        euclidean_distance_result, cos_similarity_result,
        intersection_nums, total_matches,
        length_fd, fd)

    if not is_stored and not no_save:
        store_ref(ref)
