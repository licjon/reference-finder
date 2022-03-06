# Provided Example

Example includes example_manuscript.txt that contains 4 sentences. The PDFs are in the example_refs folder. The folder contains example1.pdf and example2.pdf.

Run `python3 ref_finder.py example_manuscript.txt path/to/example_refs/` from the src directory.

The output will be output.txt. Each time the program is run, it will overwrite output.txt. Inside output.txt, you will see each sentence in the manuscript, followed by information relating to the references.

## Sentence 1

The first sentence is an example of some rare undefined behavior in this program. The first time you run this program the Jaccard Similarity will not match. However, run it again and the result derived from the json file will give the matching sentence.

The Euclidean distance and Cosine similarity sentences do not match. Sometimes they do, but Jaccard Similarity often returns the best match. The example1 also has more word matches than example2.

The results of example2 show that this reference does not support.

## Sentence 2: Jaccard, Euclidean, and Cosine all match the correct sentence from example1; example2 does not support

## Sentence 3

This is another example of less than optimal behavior: example2 has 3 matching sentences even though the scores are lower than normal (Jaccard Index of 0.2 usually does not support). This is probably because another sentence has glommed onto it.

## Sentence 4 clearly shows strong support from example2

## After running the example, example1 and example2 will be stored into the json. Delete them and leave just the "[]" before running the program with your own files.

