from euclidean_distance import euclidean_distance
import spacy

def main():
    nlp = spacy.load('en_core_web_md')
    sentences = ["The bottle is empty",
                 "There is nothing in the bottle"]
    # sentences = [sent.lower().split(" ") for sent in sentences]
    embeddings = [nlp(sentence).vector for sentence in sentences]

    distance = euclidean_distance(embeddings[0], embeddings[1])
    print(distance)

if __name__ == "__main__":
    main()
