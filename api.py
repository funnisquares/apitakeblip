from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import json
from pyngrok import ngrok
db = {'Produtos': ['Shampoo', 'Sabonete'],
        'Banho': {'Agenda':
        {'22':{'6': {'Agendado': 0}}}}}

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('Dia')
parser.add_argument('Mes')
http_tunnel = ngrok.connect()

class Produtos(Resource):
    def get(self):
        return {'Produtos': db['Produtos']}
api.add_resource(Produtos, '/produtos')

class AgendamentoBanho(Resource):

    def get(self):
        return {'Agenda': [db['Banho']['Agenda']]}

    def post(self):
        args = parser.parse_args()
        if not db['Banho']['Agenda'].get(args['Mes'], {}).get(args['Dia'], {}).get('Agendado', 0):
            db['Banho']['Agenda'][args['Mes']][args['Dia']]['Agendado'] = 1
        return db['Banho']['Agenda'][args['Mes']][args['Dia']], 201

api.add_resource(AgendamentoBanho, '/Banho')

class AgendamentoBanhoToza:
    def get(self):
        return {'Agenda': [db['Banho']['Agenda'] for agendado in db['Hotel']['Agenda'] if not agendado]}

if __name__ == '__main__':
    app.run(debug=True)