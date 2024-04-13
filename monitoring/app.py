from flask import Flask,render_template, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from bson import ObjectId
import os, json
# from database.models import Alert
from datetime import datetime, timedelta



load_dotenv()
client = MongoClient(os.environ.get('MONGO_URI'))
scheduler = BackgroundScheduler()

db = client['ksp-traffic']
node_collection = db['nodes']
event_collection = db['events']
instance_collection = db['instances']
alert_collection = db['alerts']

app = Flask(__name__)


class Alert:
    def __init__(self, event_id, node_id, start_time):
        self.event_id = event_id
        self.node_id = node_id
        self.start_time = start_time
        self.alert_time = datetime.now()


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


@app.route('/alerts')
def get_alerts():
    print("Alerts Triggered")
    check_events_for_alerts()
    alerts = list(alert_collection.find({}))
    alerts = [{
        'eventId': alert['event_id'],
        'nodeId': alert['node_id'],
        'startTime': alert['start_time'],
        'alertTime': alert['alert_time']
    } for alert in alerts]
    alerts = alerts[::-1]
    return jsonify(alerts)


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


def create_or_update_alert(event_id, node_id, start_time):
    existing_alert = alert_collection.find_one({"event_id": event_id})
    
    if existing_alert:
        alert_collection.update_one({"event_id": event_id}, {"$set": {"alert_time": datetime.now()}})
    else:
        alert = Alert(event_id, node_id, start_time)
        alert_collection.insert_one(alert.__dict__)


def check_events_for_alerts():
  
    events = event_collection.find({"end_time": None})

    for event in events:
        start_time = event['start_time']
        current_time = datetime.now()
        
 
        duration = current_time - start_time
        
 
        if duration > timedelta(minutes=15):
            print("Alert: Event duration exceeded 15 minutes")
            create_or_update_alert(event["id"], event["node_id"], event["start_time"])
            event_collection.update_one({"id": event["id"]}, {"$inc": {"alerts_raised": 1}})


scheduler.add_job(check_events_for_alerts, 'interval', minutes=6)
scheduler.start()


if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)