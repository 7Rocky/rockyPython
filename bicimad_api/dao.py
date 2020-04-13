from bicimad_api.config import *
from bicimad_api.helpers import sort_dates
from pymongo import MongoClient

class Dao:
    def __init__(self):
        mongo = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/')
        db = mongo['bicimad']
        self.bicimad = db['bicimad']
        self.bicimad_admin = db['bicimad_admin']
        self.ORIGIN = { 'column': 'idunplug_station', 'name': 'origin' }
        self.DESTINATION = { 'column': 'idplug_station', 'name': 'destination' }

    def get_number_of_dates(self):
        dates = self.bicimad.distinct('Fecha')
        dates.sort(key=sort_dates)

        return { 'count': len(dates), 'first': dates[0], 'last': dates[-1] }

    def get_stations(self, kind):
        return { 'stations': { kind['name']: self.bicimad.distinct(kind['column']) } }

    def get_movements(self, _date):
        return list(self.bicimad.find({
            'Fecha': _date
        }, {
            '_id': 0
        }))

    def get_movements_from(self, _date, _from):
        return list(self.bicimad.find({
            'Fecha': _date,
            'idunplug_station': _from
        }, {
            '_id': 0
        }))

    def get_movements_to(self, _date, _to):
        return list(self.bicimad.find({
            'Fecha': _date,
            'idplug_station': _to
        }, {
            '_id': 0
        }))

    def get_movements_from_to(self, _date, _from, _to):
        return list(self.bicimad.find({
            'Fecha': _date,
            'idunplug_station': _from,
            'idplug_station': _to
        }, {
            '_id': 0
        }))

    def get_movements_from_to_in(self, _date, _from, _to, _in, _gt):
        return list(self.bicimad.find({
            'Fecha': _date,
            'idunplug_station': _from,
            'idplug_station': _to,
            'travel_time': { '$gt' if _gt == 'true' else '$lt': _in }
        }, {
            '_id': 0
        }))

    def new_document(self, doc):
        self.bicimad.insert_one(doc)

    def update_document(self, query, update):
        result = self.bicimad.update_one(query, { '$set': update })
        return result.matched_count

    def get_users_hash(self, username):
        return self.bicimad_admin.find_one({ 'username': username }, { '_id': 0, 'hash': 1 })['hash']
