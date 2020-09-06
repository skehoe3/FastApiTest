"""
Any intake procedures required to process text should be built here.
Operations that reqire interacting with the database should be contained in db_interface.

After deciding on a data source, a csv parsing capability was added.
"""
from collections import defaultdict
from src.db_interface import Storage
from bson.objectid import ObjectId
import datetime
from pymongo.errors import BulkWriteError
from streamlit import caching

store = Storage()


def csv_to_json(file, db):
    try:
        field_names = []
        # this is of class bytes. It is the WHOLE file, not just the name.
        data = file.readlines()
        decoded = [x.decode("utf-8").strip().split(",") for x in data]
        field_names = decoded[0]
        n_fields = len(field_names)

        data_points = []
        for i in decoded[1:]:
            d = defaultdict()
            for y in range(0, n_fields-1):
                d[field_names[y]] = i[y]
            d["_id"] = ObjectId()
            d["timestamp"] = datetime.datetime.now()
            data_points.append(dict(d))

        insertions = store.insert_multiple_values(data_points, db)
        return [str(_id) for _id in insertions.inserted_ids]
    except BulkWriteError as error:
        # todo: way to remove the items that WERE succesfully inserted? before retrying insert?
        print("encountered a bulk write error. clearing cache.")
        caching.clear_cache()
        print("cleared cache.  Retrying bulk insert")
        insertions = store.insert_multiple_values(data_points, db)
        return [str(_id) for _id in insertions.inserted_ids]
    except Exception as error:
        print(f"Error in converting csv to json: {error}")
    # a set of the ids in the doohickey has only 10 items.  how on earth is there a duplicate key error?!?
    # need to clear cache and this should work:  https://stackoverflow.com/questions/43073956/pymongo-errors-bulkwriteerror-batch-op-errors-occurred-mongodb-3-4-2-pymongo
