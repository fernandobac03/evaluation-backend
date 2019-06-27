#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
from evaluationSameAs.evaluationSameAs.inter import insert_person, get_pairs_data, insert_evaluation

app = Flask(__name__)
CORS(app)

@app.route('/geolinkeddata/service/storage/add', methods=['POST'])
def add_persona():
    json = request.get_json(force=True)
    return insert_person(json)


@app.route('/geolinkeddata/service/storage/get', methods=['GET'])
def get_pairs():
    #return get_direct_results()
    if 'param' in request.args:
        param = request.args['param']
        return get_pairs_data(param)
    else:
        return "Error: No param arg provided. Please specify an id"


@app.route('/geolinkeddata/service/storage/addevaluation', methods=['POST'])
def set_evaluation():
    json = request.get_json(force=True)
    return insert_evaluation(json)


@app.route('/geolinkeddata/service/storage/test', methods=['GET'])
def test():
    return jsonify({'test': 'ok'})

   
if __name__ == '__main__':
    app.run(debug=True)







