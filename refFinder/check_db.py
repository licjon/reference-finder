from pathlib import Path
import json


def check_db(ref_file):
    """Returns dictionary if PDF found in json; returns None if not found."""
    file_path = Path(ref_file)
    file_name = file_path.stem
    
    with open('references.json', 'r') as references:
        refs_data = references.read()

    refs_dict = json.loads(refs_data)
        
    ref_dict = None 
    for key in refs_dict:
        # print(str(type(refs_dict[key])))
        for dic in refs_dict[key]:
            # print(str(dic["name"]))
            if (dic["name"]) == file_name:
                # print(file_name + " is true")
                ref_dict = dic
                break
            else: continue
            # print(file_name + " is false")
            ref_dict = None

    return ref_dict
