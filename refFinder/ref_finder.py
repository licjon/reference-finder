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
    with open(firstfile, 'r') as ff, open(secondfile, 'r') as sf:
        ff_words = ff.read().split()
        sf_words = sf.read().split()

    # Finds intersection of words in the 2 lists
    intersection_words = [word for word in ff_words if (word in sf_words)
                          and (word not in set(stopwords.words('english')))]

    # counts the frequency of each intersected word, discarding common words
    fd = FreqDist(word for word in sf_words if word in intersection_words)
    length_fd = len(fd)
    total_matches = sum(fd.values())
    fd.pprint()
    print(total_matches)

except IOError:
    print("Could not read from file")
    exit(1)
