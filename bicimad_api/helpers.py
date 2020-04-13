import datetime
import re

FIELDS = { 'Fecha', 'idunplug_station', 'idplug_station', 'idunplug_base',
            'idplug_base', 'travel_time', 'ageRange', 'user_type', 'Fichero' }

def sort_dates(date_string):
    day, month, year = date_string.split('/')
    return datetime.datetime(int(year), int(month), int(day)).timestamp()

def verify_date(date):
    if date is None:
        return False

    if not re.search('^((0[1-9]|[12]\d|3[01])\/(0[1-9]|1[0-2])\/[12]\d{3})$', date):
        return False
    
    if date.startswith('31/04') or date.startswith('31/06') or \
        date.startswith('31/09') or date.startswith('31/11') or \
        date.startswith('30/02') or date.startswith('31/02'):
        return False

    if date.startswith('29/02') and int(date[8:10]) % 4 != 0:
        return False

    return True

def verify_doc(doc):
    if len(doc) == len(FIELDS) and all(key in FIELDS for key in doc.keys()):
        if verify_date(doc['Fecha']) and type(doc['Fichero']) == int and \
            type(doc['idunplug_station']) == int and type(doc['idplug_station']) == int and \
            type(doc['idunplug_base']) == int and type(doc['idplug_base']) == int and \
            type(doc['ageRange']) == int and type(doc['user_type']) == int and \
            type(doc['travel_time']) == int:

            if doc['idunplug_base'] >= 1 and doc['idunplug_base'] <= 30 and \
                doc['idplug_base'] >= 1 and doc['idplug_base'] <= 30 and\
                doc['idunplug_station'] >= 1 and doc['idplug_station'] >= 1 and \
                doc['ageRange'] >= 0 and doc['ageRange'] <= 6 and \
                doc['user_type'] >= 1 and doc['user_type'] <= 3 and \
                doc['travel_time'] >= 0 and doc['Fichero'] >= 0:

                return True

    return False
