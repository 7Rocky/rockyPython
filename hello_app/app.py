from cloudant import Cloudant
from flask import Flask, jsonify, render_template, request

import atexit
import json
import os

def main(app):
    app.static_url_path = 'hello_app/static/'
    app.static_folder = 'hello_app/static/'
    db_name = 'my-db-2'
    client = None
    db = None

    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.getenv('VCAP_SERVICES'))
        print('Found VCAP_SERVICES')

        if 'cloudantNoSQLDB' in vcap:
            creds = vcap['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
    elif 'CLOUDANT_URL' in os.environ:
        client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
    elif os.path.isfile('vcap-local.json'):
        with open('vcap-local.json') as f:
            vcap = json.load(f)
            print('Found local VCAP_SERVICES')
            creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
            print(db)

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    @app.route('/api/visitors')
    def get_visitor():
        if client:
            return jsonify(list(map(lambda doc: doc.get('name'), dict(db).values())))
        else:
            print('No database')
            return jsonify([])

    @app.route('/api/visitors', methods=['POST'])
    def put_visitor():
        user = request.json['name']
        data = { 'name': user }

        if client:
            my_document = db.create_document(data)
            data['_id'] = my_document['_id']
            return jsonify(data)
        else:
            print('No database')
            return jsonify(data)

    @atexit.register
    def shutdown():
        if client:
            client.disconnect()
