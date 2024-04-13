from flask import Flask,render_template, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()
import os, json
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['ksp-traffic']
node_collection = db['nodes']
event_collection = db['events']
instance_collection = db['instances']

app = Flask(__name__)

@app.route("/")
def home():
    result = node_collection.find({})
    results = []
    for i in result:
        results.append({
            'id': i['id'],
            'latitude': i['latitude'],
            'longitude': i['longitude'],
            'name': i['name'],
            'address': i['address'],
        })

    return render_template('home.html', result=results)


@app.route('/alert')
def alert():
    pass
    #prometheus code to create an alert.

@app.route('/data')
def get_data():
   
    total_nodes = node_collection.count_documents({})
    total_vehicles = instance_collection.count_documents({})

   
    data = {
        'totalNodes': total_nodes,
        'totalVehicles': total_vehicles,
    }
    print(data)
    return jsonify(data)


@app.route('/events/<int:node_id>', methods=['GET'])
def get_events(node_id):
    result = event_collection.find({"node_id": node_id})
    result = list(result)
    result = [{**event, '_id': str(event['_id'])} for event in result]

    print(result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)