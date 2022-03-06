# Reference Finder

 Reference Finder will compare each sentence in the manuscript to each reference and help you find which reference supports the sentence in the manuscript as well as provide sentences from each reference that are most likely to give support.

 Essentially, this program takes a text or docx file and compares each sentence to each sentence in multiple PDFs and returns information about what has matched in each PDF, such as:

- Total words matched

- The number of individual words matched

- The frequency of each matched word

- Numbers matched

- 1-3 sentences that may closely match the sentence in the given text file. These are determined by:

    1.  Jaccard similarity

    2.  Euclidean distance

    3.  Cosine similarity

 The application I thought of for this program was to find supporting references for a manuscript, hence the name Reference Finder. The manuscript is the text file (.txt) or Word doc file (.docx). References are PDF files. But this can be used for any purpose that requires matching sentences in a text or word file to text in PDFs.

## How to run

1. Clone repo

2. In terminal, cd into the repo's directory and run `virtualenv env`

3. Then run `source env/bin/activate`

4. Then run `pip install -r requirements.txt`

5. Your manuscript (txt or docx) and subdirectory of PDFs should be in the src directory but don't have to be.

6. cd into the src directory and run `python3 ref_finder.py file_name.txt path/to/pdf/folder/`. If your manuscript file is in another directory, then enter the path to the file (including the file name) instead of just the file name.

7. After you run it the first time, the PDFs are stored in a json file. If you want to use those references again, you can run the same command but without the path to the references folder. If you have many references stored in the json, but only want to compare select references, use a path to a directory with those references, and it will just use those references (it uses the file names to search for them in the json file).

## Examples

Running a docx file in another directory and using all references in the json: 
```bash
python3 ref_finder.py ~/path/to/file.docx
```

### Some optional flags are:

`--nosave`
- Doesn't save the references to the json file.
- Even though it doesn't make sense to run this without a file path, it will still run but uses the json file.
- Example: 
```bash
python3 ref_finder.py file.docx ~/path/to/folder/ --nosave
 ```

`--nodb`
- Doesn't use the json file and reads the PDFs.
- --nodb will not work unless a filepath is provided.
- A situation where this could be useful is if you have a large json file but only want to use a few PDFs. It will run faster.
- Example: 
```bash
python3 ref_finder.py file.txt ~/path/to/folder/ --nodb
```

`--help`
- Displays help

## Limitations

The PDF files must be searchable PDFs. If not, try to use optical character recognition to make a searchable PDF before using Reference Finder. The PDF file format has a broad specification and is not designed for data exchange. This makes PDFs particularly hard to read. Reference Finder used PyPDF2, and if that fails, PDFMiner, and may output a message that the PDF is not readable. Even then, some PDFs will return unreadable garbage (Of the 70 PDFs that I tested, 4 were not readable at all). This will hopefully be addressed in a later version. A possible approach would be to read XML/ePub versions of the articles as XML is machine readable, with the hopes that XML will surpass PDF as the predominant format for online publications.

### False negatives
Supporting information that is in a table or graph will probably not be read and matched.
