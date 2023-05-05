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

def data_point_remover(obs_data, index):
    import numpy as np
    removed_data = obs_data.copy()
    for key in obs_data.keys():
        removed_data[key] = np.array(obs_data[key])[index].tolist()
        obs_data[key] = np.delete(obs_data[key], index).tolist()
    return obs_data, removed_data

def sort(obs_data):
    """
    Sorts a dict of obs data (e.g. my_data["GBM_data"]) by date.
    """
    print("Sorting...")
    data = obs_data.copy()
    i = 0
    while i < len(data["dates"]):
        j = 1
        while j < len(data["dates"]):
            if data["dates"][j] < data["dates"][j-1]:
                for key in data.keys():
                    tmp = data[key][j]
                    data[key][j] = data[key][j-1]
                    data[key][j-1] = tmp
            j += 1
        i += 1
    return data


def add_data(obs_data, new_data):
    """
    Add some new data to the set and sort them.
    """
    print("Adding the data...")
    data = obs_data.copy()
    for key in data.keys():
        if type(new_data[key]) != list:
            data[key] = [new_data[key]]
        data[key] += new_data[key]

    data = sort(data)
    print("Done!")
    return data
