from sys import argv
# from nltk.tokenize import wordpunct_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from PyPDF2 import PdfFileReader

# Allows program to run with args
script, firstfile, secondfile = argv

# Need to handle numbers and remove symbols and add words to stopwords

# Counts occurences in second file of intersection of words in 2 files
try:
    # Opens files and split them into lists of words
    with open(firstfile, 'r') as ff:  # , open(secondfile, 'r') as sf:
        ff_words = ff.read().split()
#        sf_words = sf.read().split()
        ff.close()

    with open(firstfile, 'r') as ff:  # , open(secondfile, 'r') as sf:
        ff_str = ff.read().replace("\n", " ")

    # Read pdf file
    sf = PdfFileReader(secondfile)
    sf_pages = []
    # Extract pdf and split into words
    # (list of list is a page (list) of a list of string)
    for page in sf.pages:
        sf_pages.append(page.extractText().split())

    sf_words = [word for page in sf_pages for word in page]

    # Finds intersection of words in the 2 lists
    intersection_words = [word for word in ff_words if (word in sf_words)
                          and (word not in set(stopwords.words('english')))]

    # counts the frequency of each intersected word, discarding common words
    fd = FreqDist(word for word in sf_words if word in intersection_words)
    total_matches = sum(fd.values())

    # fd.pprint()
    # print(total_matches)
    # print(length_fd)
    # print(ff_str)
    # print(secondfile)

    length_fd = len(fd)
    with open('output.txt', 'w') as output:
        lines = [ff_str, "\n", "\n", secondfile, ":", "\n",
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

except IOError:
    print("Could not read from file")
    exit(1)
