from pathlib import Path
import json


def check_db(ref_file):
    """Returns dictionary if PDF found in json; returns None if not found."""
    # TODO Try search algorithm?
    file_path = Path(ref_file)
    file_name = file_path.stem
    
    with open('references.json', 'r') as references:
        refs_data = references.read()

    refs_dict = json.loads(refs_data)
    # ref_dict = None 
    front = 0
    back = len(refs_dict) - 1

    # Front and back search for reference in json
    if refs_dict != []:
        while front <= back:
            middle = (front + back) // 2
            midpoint = refs_dict[middle]
            if midpoint["name"] > file_name:
                back = middle - 1
            elif midpoint["name"] < file_name:
                front = middle + 1
            else:
                return midpoint

