def write_results(file_name, intersection_nums, total_matches, length_fd, fd, top_scoring_sentence):
    """Write results of comparisons to output text file."""
    try:
        # Writes fd, total_matches, length_fd to output file
        with open('output.txt', 'a') as output:
            lines = ['\n', "Reference: ", file_name, "\n",
                     "Jaccard Similarity: ", str(top_scoring_sentence), "\n",
                     "Numbers matched: ", str(intersection_nums), "\n",
                     "Total matches: ", str(total_matches), "\n",
                     "Number of words matched: ", str(length_fd), "\n",
                     "Words matched: "]
            output.writelines(lines)

        with open('output.txt', 'a') as output:
            # output.write(str(fd.most_common(20)))
            output.write(', '.join("{}: {}".format(k, v)
                                   for k, v in fd.items()))

        with open('output.txt', 'a') as output:
            output.write('\n')

    except IOError:
        print("write_results: Could not append to file")
        exit(1)
