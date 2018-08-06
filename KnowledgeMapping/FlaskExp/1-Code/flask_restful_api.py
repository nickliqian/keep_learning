# -*- coding: UTF-8 -*-
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

data = {
    '1': {'task': 'Python'},
    '2': {'task': 'Java'},
    '3': {'task': 'GoLang'},
}


def abort_if_todo_doesnt_exist(data_id):
    print(data_id not in data)
    if data_id not in data:
        abort(404, message="Operate {} doesn't exist".format(data_id))


parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# operate
class Operate(Resource):
    def get(self, data_id):
        abort_if_todo_doesnt_exist(data_id)
        return data[data_id]

    def delete(self, data_id):
        abort_if_todo_doesnt_exist(data_id)
        del data[data_id]
        return '', 204

    def put(self, data_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        data[data_id] = task
        return task, 201


# show data
class GetData(Resource):
    def get(self):
        return data

    def post(self):
        args = parser.parse_args()
        data_id = int(max(data.keys()).lstrip('todo')) + 1
        data_id = 'todo%i' % data_id
        data[data_id] = {'task': args['task']}
        return data[data_id], 201


# Actually setup the Api resource routing here
api.add_resource(Operate, '/operate')
api.add_resource(GetData, '/getdate/<data_id>')

if __name__ == '__main__':
    app.run(debug=True, port=9800)
