from flask import Flask
from flask_restful import Resource, Api,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'

# Fake database
fakeDatabase = {
    1: {'name': 'wake up'},
    2: {'name': 'cook'},
    3: {'name': 'clean'},
}

# Resource to get all items
class Items(Resource):
    def get(self):
        task=Task.query.all()
        return task
    
    def post(self):
        data=request.json
        task=Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        task=Task.query.all()
        return task
# Resource to get a specific item by its primary key (pk)
class Item(Resource):
    def get(self, pk):
        task=Task.query.filter_by(id=pk).first()
        return fakeDatabase.get(pk, {'error': 'Item not found'})

# Add the resources to the API
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
