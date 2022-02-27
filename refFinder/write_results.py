def write_results(file_name, top_scoring_sentence, euclidean_distance,
                  cos_similarity, intersection_nums, total_matches,
                  length_fd, fd):
    """Write results of comparisons to output text file."""
    # Writes fd, total_matches, length_fd to output file
    with open("output.txt", 'a') as output:
        lines = [
            '\n', "Reference: ", file_name, "\n\n",
            "Jaccard Similarity: ", str(top_scoring_sentence), "\n\n",
            "Euclidean Distance: ", str(euclidean_distance), "\n\n", 
            "Cos Similarity: ", str(cos_similarity), "\n\n",
            "Numbers matched: ",
            str(intersection_nums), "\n\n",
            "Total matches: ", str(total_matches), '\n',
            "Number of words matched: ", str(length_fd), '\n',
            "Words matched: "
        ]
        output.writelines(lines)

    with open("output.txt", 'a') as output:
        output.write(', '.join("{}: {}".format(k, v)
                               for k, v in fd.items()))

    with open("output.txt", 'a') as output:
        output.write('\n')
