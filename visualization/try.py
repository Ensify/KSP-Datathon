import pymongo
from datetime import datetime
import os
from flask import Flask, render_template, request, jsonify
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
client = pymongo.MongoClient(os.environ.get("MONGO_URI"))
db = client['ksp-traffic']
node_collection = db['nodes']

@app.route('/get_data', methods=['GET'])
def get_data():
    node_id = request.args.get('node_id')
    type = request.args.get('type')

    timestamps = []
    count = []
    print(node_id, type)
    if type == "People Count":
        collection = db["instances"]
        data = collection.find({'node_id': int(node_id)})
        print("Docs Count" )

        for document in data:
            timestamps.append(document['time_stamp'])
            count.append(document['people_count'])

    elif type == "Vehicle Count":
        collection = db["instances"]
        data = collection.find({'node_id': int(node_id)})
        print("Docs Count" )

        for document in data:
            timestamps.append(document['time_stamp'])
            count.append(document['vehicle_count'])

    elif type == "Parked Vechicle Count":
        print("here....")
        collection = db["instances"]
        data = collection.find({'node_id': int(node_id)})
        print("Docs Count" )
        for document in data:
            timestamps.append(document['time_stamp'])
            count.append(document['parked_vehicle_count'])


    print(timestamps, count)
    sorted_data = sorted(zip(timestamps, count))
    sorted_timestamps, sorted_count = zip(*sorted_data)

    return jsonify({'timestamps': sorted_timestamps, 'count': sorted_count})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        node_id = request.form.get('node_id')
        type = request.form.get('type')
   

    result = node_collection.find({})
    results = []
    for i in result:
        results.append({
            'id': i['id'],
            'name': i['name'],
            'address': i['address'],
        })

    types = ["Parked Vechicle Count", "Vehicle Count", "People Count"]

    return render_template('index.html', results=results, types=types)

if __name__ == '__main__':
    app.run(debug=True)
