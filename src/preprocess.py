"""
Any intake procedures required to process text should be built here. 
Operations that reqire interacting with the database should be contained in db_interface.

After deciding on a data source, a csv parsing capability was added. 
"""
from collections import defaultdict
from src.db_interface import Storage

store = Storage()


def csv_to_json(file, db):
    # each row should be read into the db as a seperate sample
    # BUT - they share keys, which are in the first row of the file
    field_names = []
    # this is of class bytes. It is the WHOLE file, not just the name.
    data = file.readlines()
    # with open(data, 'r') as f:  # this expects the file name -- not the file itself
    #     x = f.readlines()
    decoded = [x.decode("utf-8").strip().split(",") for x in data]
    field_names = decoded[0]
    n_fields = len(field_names)

    for i in decoded[1:]:
        d = defaultdict()
        for y in range(0, n_fields-1):
            d[field_names[y]] = i[y]
        store.insert_value(d, db)
