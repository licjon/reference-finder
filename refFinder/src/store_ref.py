import json

from operator import itemgetter


def store_ref(ref):
    """Store reference class data as json"""
    ref_data = {"name": ref.name, "sentences": ref.sentences,
                "words": ref.words}

    with open("references.json", 'r+') as json_file:
        json_data = json.load(json_file)
        json_data.append(ref_data)
        json_file.seek(0)
        json_data = sorted(json_data, key=itemgetter("name"))
        json.dump(json_data, json_file, indent=4)
