from pathlib import Path
import json


def check_db(ref_file):
    file_path = Path(ref_file)
    file_name = file_path.stem
    
    with open('references.json', 'r') as references:
        refs_data = references.read()

    refs_dict = json.loads(refs_data)
        
    # if any(file_name in refs_dict.values() for d in refs_dict.values()):
    #     return True
    # else:
    #     print("false")
    is_stored = False 
    for key in refs_dict:
        # print(str(type(refs_dict[key])))
        for dic in refs_dict[key]:
            print(str(dic["name"]))
            # for ref_key in dic:
            if (dic["name"]) == file_name:
                print(file_name + " is true")
                is_stored = True
                break
            else: continue
            print(file_name + " is false")
            is_stored = False

    return is_stored
