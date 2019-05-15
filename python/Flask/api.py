from flask import Flask, request
from flask_restful import Api, Resource
"""
git checkout min_restful
"""

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id:todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}
api.add_resource(TodoSimple, '/<string:todo_id>')
#api.add_resource(TodoSimple, '/')

if __name__ == '__main__':
    app.debug = True
    app.run()