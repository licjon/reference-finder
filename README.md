



<a id="orgd414e7e"></a>

# What is Reference Finder?



<a id="org8d73516"></a>

## Reference Finder will compare each sentence in the manuscript to each reference and help you find which reference supports the sentence in the manuscript as well as provide sentences from each reference that are most likely to give support.


<a id="orgb1994f4"></a>

## Essentially, this program takes a text or docx file and compares each sentence to each sentence in multiple PDFs and returns information about what has matched in each PDF, such as:


<a id="orge8bc44f"></a>

### Total words matched


<a id="orgd6d4b07"></a>

### The number of individual words matched


<a id="org6863f12"></a>

### The frequency of each matched word


<a id="orgf4e6e35"></a>

### Numbers matched


<a id="orga5aa16f"></a>

### 1-3 sentences that may closely match the sentence in the given text file. These are determined by:

1.  Jaccard similarity

2.  Euclidean distance

3.  Cosine similarity


<a id="org0b5669c"></a>

## The application I thought of for this program was to find supporting references for a manuscript, hence the name Reference Finder. The manuscript is the text file (.txt) or Word doc file (.docx). References are PDF files. But this can be used for any purpose that requires matching sentences in a text or word file to text in PDFs.


<a id="how-to-run"></a>

# How to run



<a id="orgac3c093"></a>

## ref<sub>finder.py</sub> is run from the command line. cd into the directory that has ref<sub>finder.py</sub>. Your manuscript (txt or docx) and subdirectory of PDFs should be in the same directory but don't have to be.


<a id="orgb73b856"></a>

## Run `python3 ref_finder.py file_name.txt path/to/pdf/folder/`. If your manuscript file is in another directory, then enter the path to the file (including the file name) instead of just the file name.


<a id="orga9125b0"></a>

## After you run it the first time, the PDFs are stored in a json file. If you want to use those references again, you can run the same command but without the path to the references folder. If you have many references stored in the json, but only want to compare select references, use a path to a directory with those references, and it will just use those references (it uses the file names to search for them in the json file).


<a id="orgcfc579e"></a>

### Example of running a docx file in another directory and using all references in the json: `python3 ref_finder.py ~/path/to/file.docx`


<a id="orge18a6ea"></a>

## Some optional flags are:


<a id="org7df1dc5"></a>

### &#x2013;nosave

1.  Doesn't save the references to the json file.

2.  Even though it doesn't make sense to run this without a file path, it will still run but uses the json file.

3.  Example:  `python3 ref_finder.py file.docx ~/path/to/folder/ --nosave`


<a id="org327fbd4"></a>

### &#x2013;nodb

1.  Doesn't use the json file and reads the PDFs.

2.  &#x2013;nodb will not work unless a filepath is provided.

3.  A situation where this could be useful is if you have a large json file but only want to use a few PDFs. It will run faster.

4.  Example:  `python3 ref_finder.py file.txt ~/path/to/folder/ --nodb`


<a id="orga4c954c"></a>

### &#x2013;help


<a id="org4589da0"></a>

# Limitations


<a id="orga947972"></a>

## The PDF files must be searchable PDFs. If not, try to use optical character recognition to make a searchable PDF before using Reference Finder. The PDF file format has a broad specification and is not designed for data exchange. This makes PDFs particularly hard to read. Reference Finder used PyPDF2, and if that fails, PDFMiner, and may output a message that the PDF is not readable. Even then, some PDFs will return unreadable garbage (Of the 70 PDFs that I tested, 4 were not readable at all). This will hopefully be addressed in a later version. A possible approach would be to read XML/ePub versions of the articles as XML is machine readable, with the hopes that XML will surpass PDF as the predominant format for online publications.


<a id="org2f4801f"></a>

## False negatives


<a id="org8083ff2"></a>

### Supporting information that is in a table or graph will probably not be read and matched.


<a id="orgd6e59d9"></a>

# Provided Example


<a id="orge2994de"></a>

## Example includes example<sub>manuscript.txt</sub> that contains 4 sentences. The PDFs are in the example<sub>refs</sub> folder. The folder contains example1.pdf and example2.pdf.


<a id="org140c04d"></a>

## Download the repository


<a id="org7288076"></a>

## Run `python3 ref_finder.py example_manuscript.txt path/to/example_refs/` from the directory ref<sub>finder.py</sub> is in


<a id="orgeed8432"></a>

## The output will be output.txt. Each time the program is run, it will overwrite output.txt.


<a id="org9cb6c13"></a>

## Inside output.txt, you will see each sentence in the manuscript, followed by information relating to the references


<a id="orgf47d4d7"></a>

## Sentence 1


<a id="orgb8ebe97"></a>

### The first sentence is an example of some rare undefined behavior in this program. The first time you run this program the Jaccard Similarity will not match. However, run it again and the result derived from the json file will give the matching sentence.


<a id="org850cdda"></a>

### The Euclidean distance and Cosine similarity sentences do not match. Sometimes they do, but Jaccard Similarity often returns the best match


<a id="orgde015ad"></a>

### The example1 also has more word matches than example2


<a id="orge431bed"></a>

### The results of example2 show that this reference does not support


<a id="orgc086642"></a>

## Sentence 2: Jaccard, Euclidean, and Cosine all match the correct sentence from example1; example2 does not support


<a id="org2ebfa03"></a>

## Sentence 3


<a id="org145c0fd"></a>

### This is another example of less than optimal behavior: example2 has 3 matching sentences even though the scores are lower than normal (Jaccard Index of 0.2 usually does not support). This is probably because another sentence has glommed onto it.


<a id="orgce65bbd"></a>

## Sentence 4 clearly shows strong support from example2


<a id="org89023ad"></a>

## After running the example, example1 and example2 will be stored into the json. Delete them and leave just the "[]" before running the program with your own files.

