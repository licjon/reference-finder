def intersection_numbers(sentence, ref_words):
    """Find the interesection of numbers in sentence and numbers in a reference pdf."""
    
    # Create list of intersecting numbers
    manuscript_nums = []
    for grapheme in sentence:
        try:
            if float(grapheme):
                manuscript_nums.append(grapheme)
        except ValueError:
            continue
        
    intersection_nums = [
        num for num in manuscript_nums if (num in ref_words)]

    return intersection_nums

