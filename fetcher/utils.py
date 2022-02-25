import json

def write_file_from_list(filename, data):
    f = open(filename, "w")
    data.sort()
    for item in data:
        f.write(f"{item}\n")
    f.close()

def write_file(filename, data):
    if ".json" in filename:
        data = json.dumps(data, indent=4)
    f = open(filename, "w")
    f.write(data)
    f.close()
