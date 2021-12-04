"""Finds supporting references for manuscript."""
from sys import argv
# from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from PyPDF2 import PdfFileReader
# from pathlib import Path
import os
import glob


def get_words(firstfile, secondfile):
    """Count occurences in second file of intersection of words in 2 files."""
    try:
        # Opens text file and splits it into lists of words
        with open(firstfile, 'r') as ff:  # , open(secondfile, 'r') as sf:
            ff_words = ff.read().split()
            #        sf_words = sf.read().split()
            ff.close()

        # Read pdf file
        sf = PdfFileReader(secondfile)
        sf_pages = []

        # Extract pdf and split into words
        # (list of list is a page (list) of a list of string)
        for page in sf.pages:
            sf_pages.append(page.extractText().split())

        # Creates list of words in pdf
        sf_words = [word for page in sf_pages for word in page]

        # Creates list of intersection of words in the 2 lists
        intersection_words = [
            word for word in ff_words if (word in sf_words)
            and (word not in set(stopwords.words('english')))]

        # Dictionary of frequency of each intersected word,
        # discarding common words
        fd = FreqDist(word for word in sf_words if word in intersection_words)

        total_matches = sum(fd.values())

        # Number of words matched
        length_fd = len(fd)

        # Writes fd, total_matches, length_fd to output file
        with open('output.txt', 'a') as output:
            lines = [secondfile, ":", "\n",
                     "Number of words matched: ", str(length_fd), "\n",
                     "Total matches: ", str(total_matches), "\n",
                     "Words matched: "]
            output.writelines(lines)
            output.close()

        with open('output.txt', 'a') as output:
            # output.write(str(fd.most_common(20)))
            output.write(', '.join("{}: {}".format(k, v)
                                   for k, v in fd.items()))
            output.close()

        with open('output.txt', 'a') as output:
            output.write('\n')
            output.close()

    except IOError:
        print("Could not read from file")
        exit(1)


def main():
    """Do the main function."""
    # Arguments. Run "python ref_finder.py file.txt ~/path/to/pdf/directory"
    script, firstfile, directory = argv

    try:
        # Opens text file and convert to string
        # TODO: Iterate over many sentences
        # TODO: Make into function outside of main
        with open(firstfile, 'r') as ff:  # , open(secondfile, 'r') as sf:
            ff_str = ff.read().replace("\n", " ")

        # Writes contents of input text file (1 sentence for now) to output.txt
        # TODO: Make into function outside of main
        with open('output.txt', 'w') as output:
            lines = [ff_str, "\n", "\n"]
            output.writelines(lines)
            output.close()

        # Creates a list of paths
        files = glob.glob(os.path.join(directory, '*.pdf'))

        # Iterate through list of paths and call get_words
        for file in files:
            get_words(firstfile, file)

    except IOError:
        print("Could not read from file")
        exit(1)


if __name__ == "__main__":
    main()
