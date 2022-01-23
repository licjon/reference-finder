sentence = ['there', 'are', '10', 'cats', 'in', '10.1', 'houses', '.']

def find_num(sentence):
    for grapheme in sentence:
        try:
            if float(grapheme):
                print(grapheme)
        except ValueError:
            pass
