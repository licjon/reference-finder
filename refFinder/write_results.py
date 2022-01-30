def write_results(file_name, top_scoring_sentence, euclidean_distance, cos_similarity):
    """Write results of comparisons to output text file."""
    try:
        # Writes fd, total_matches, length_fd to output file
        with open('output.txt', 'a') as output:
            lines = ["\n", "Reference: ", file_name, "\n",
                     "Jaccard Similarity: ", str(top_scoring_sentence[0]), "\n",
                     str(top_scoring_sentence[1]), "\n", str(top_scoring_sentence[2]), "\n\n", 
                     "Euclidean Distance: ", str(euclidean_distance[0]), "\n", 
                     str(euclidean_distance[1]), "\n", str(euclidean_distance[2]),
                     "\n\n",
                     "Cos Similarity: ", str(cos_similarity[0]), "\n",
                     str(cos_similarity[1]), "\n", str(cos_similarity[2]), "\n"
                     # "Numbers matched: ",
                     # str(intersection_nums), "\n\n",
                     # "Total matches: ", str(total_matches), "\n",
                     # "Number of words matched: ", str(length_fd), "\n",
                     # "Words matched: "
                     ]
            output.writelines(lines)

        # with open('output.txt', 'a') as output:
            # output.write(', '.join("{}: {}".format(k, v)
                                   # for k, v in fd.items()))

        with open('output.txt', 'a') as output:
            output.write('\n')

    except IOError:
        print("write_results: Could not append to file")
        exit(1)
