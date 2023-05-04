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
