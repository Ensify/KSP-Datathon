from flask import Flask,render_template
from pymongo import MongoClient
from dotenv import load_dotenv
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
            'latitude': i['latitude'],
            'longitude': i['longitude'],
            'name': i['name'],
            'address': i['address'],
        })

    return render_template('home.html', result=results)



if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)