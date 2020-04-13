from bicimad_api.dao import Dao
from flask import Flask, jsonify, redirect, request
from flask_caching import Cache
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from bicimad_api.helpers import verify_date, verify_doc

import hashlib
import json

def main(app):
    cache = Cache(config={ 'CACHE_TYPE': 'simple' })
    cache.init_app(app)
    CORS(app)
    auth = HTTPBasicAuth()
    dao = Dao()
    endpoint = '/bicimad-api/v1.0'

    @app.route(f'{endpoint}/docs')
    def get_docs():
        return redirect('https://rockyPython.mybluemix.net/docs', code=302)

    @app.route(f'{endpoint}/dates')
    @cache.cached(timeout=60)
    def get_dates():
        return dao.get_number_of_dates()

    @app.route(f'{endpoint}/stations/<string:kind>')
    @cache.cached(timeout=60)
    def get_stations(kind):
        if kind == dao.ORIGIN['name']:
            return dao.get_stations(dao.ORIGIN)
        elif kind == dao.DESTINATION['name']:
            return dao.get_stations(dao.DESTINATION)
        else:
            return { 'error': 'Not Found' }, 404

    @app.route(f'{endpoint}/movements')
    @cache.cached(timeout=60, query_string=True)
    def get_movements():
        _date = request.args.get('date')
        _from = request.args.get('from')
        _to = request.args.get('to')

        try:
            if verify_date(_date):
                if all((_from, _to)):
                    return jsonify(dao.get_movements_from_to(_date, int(_from), int(_to)))
                elif _from is not None and _to is None:
                    return jsonify(dao.get_movements_from(_date, int(_from)))
                elif _from is None and _to is not None:
                    return jsonify(dao.get_movements_to(_date, int(_to)))
                elif _from is None and _to is None:
                    return jsonify(dao.get_movements(_date))
        except ValueError:
            pass

        return { 'error': 'Some parameters are wrong' }, 400

    @app.route(f'{endpoint}/movements/time')
    @cache.cached(timeout=60, query_string=True)
    def get_movements_time():
        _date = request.args.get('date')
        _from = request.args.get('from')
        _to = request.args.get('to')
        _in = request.args.get('in')
        _gt = request.args.get('gt')

        try:
            if verify_date(_date) and None not in (_from, _to, _in):
                return jsonify(dao.get_movements_from_to_in(_date, int(_from), int(_to), int(_in), _gt))
        except ValueError:
            pass

        return { 'error': 'Some parameters are wrong' }, 400

    @auth.verify_password
    def verify_password(username, password):
        if all((username, password)):
            return hashlib.sha256(password.encode()).hexdigest() == dao.get_users_hash(username)

    @app.route(f'{endpoint}/new', methods=['POST'])
    @auth.login_required
    def new():
        data = request.json

        if data is not None:
            data['Fichero'] = 0

            if verify_doc(data):
                dao.new_document(data.copy())
                cache.clear()
                return jsonify(data), 201

        return { 'error': 'Some fields/values are invalid. Please, check the API documentation' }, 400

    @app.route(f'{endpoint}/time/update', methods=['PUT'])
    def time_update():
        data = request.json

        if verify_doc(data):
            query = data.copy()

            travel_time = query.pop('travel_time')

            if dao.update_document(query, { 'travel_time': travel_time }):
                cache.clear()
                return jsonify(data), 200
            else:
                return { 'error': 'Document not found in the database' }, 404
        else:
            return { 'error': 'Some fields are invalid' }, 400
