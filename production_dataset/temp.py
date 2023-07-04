def load_names_into_set(filename):
    names = set()
    with open(filename) as fhand:
        for row in fhand:
            names.add(row.split(" ")[0].lower())
    return names

print(load_names_into_set("../raw_data/firstnames"))