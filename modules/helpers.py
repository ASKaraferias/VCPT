negatives = ['no', 'NO', 'No', 'n', 'N', 'nO']
positives = ['yes', 'YES', 'Yes', 'yEs', 'yeS', 'yES', 'YEs', 'YeS', 'y', 'Y']

def importjson():
    import json
    while True:
        print()
        filename = input("Provide the json file: ").strip()
        try:
            json_file = open(filename, "r")
            data = json.load(json_file)
            print()
            print("Success!")
            print()
            break
        except:
            print("Please provide a valid json file!")
    return data

def exportjson(my_data):
    import json
    import os
    json_data = json.dumps(my_data)
    while True:
        print()
        filename = input("Where do you want to save the file? ")
        if os.path.isdir(filename):
            try:
                filename += "vcpt_save.json"
                file = open(filename, "w")
                file.write(json_data)
                print()
                print("Success!")
                print()
                break
            except:
                print("Sorry, I couldn't write in that directory!")
        else:
            try:
                file = open(filename, "w")
                file.write(json_data)
                print()
                print("Success!")
                print()
                break
            except:
                print("Please provide a valid filename!")

def restrict_by_date(obs_data, start, stop):
    """
    Arguments: obs_data (dictionary, e.g. 'my_data["GBM_data"]'), start date, stop date
    Returns: obs_data restricted to the data between the start date and stop date
    """
    import numpy as np
    old_dates = np.array(obs_data["dates"])
    for key in obs_data.keys():
        obs_data[key] = np.array(obs_data[key])
        obs_data[key] = obs_data[key][old_dates >= start][old_dates[old_dates >= start] <= stop].tolist()
    return obs_data

