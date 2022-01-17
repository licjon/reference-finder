def read_manuscript(manuscript):
    """Read text file and return string of contents."""
    try:
        # Opens text file and convert to string
        with open(manuscript, 'r') as manuscript:
            manuscript_string = manuscript.read().replace("\n", " ")

        return manuscript_string

    except IOError:
        print("read_manuscript: Could not read from file")
        exit(1)
