from flask import Flask,render_template, jsonify, request
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from bson import ObjectId
import os, json
# from database.models import Alert
from datetime import datetime, timedelta
import plotly.graph_objs as go


load_dotenv()
client = MongoClient(os.environ.get('MONGO_URI'))
scheduler = BackgroundScheduler()

db = client['ksp-traffic']
node_collection = db['nodes']
event_collection = db['events']
instance_collection = db['instances']
alert_collection = db['alerts']
vehicle_collection = db['vehicles']


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

    return render_template('index.html', result=results)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/alerts')
def get_alerts():
    print("Alerts Triggered")
    check_events_for_alerts()
    alerts = list(alert_collection.find({}))
    alerts = [{
        'eventType': event_collection.find_one({'id':alert['event_id']})['type'],
        'alerts': event_collection.find_one({'id':alert['event_id']})['alerts_raised'],
        'nodeId': node_collection.find_one({'id':alert['node_id']})['name'],
        'startTime': alert['start_time'],
        'alertTime': alert['alert_time']
    } for alert in alerts]
    alerts = alerts[::-1]
    return jsonify(alerts)

@app.route('/alerts/active')
def get_active_alerts():
    print("Alerts Triggered")
    check_events_for_alerts()
    alerts = list(alert_collection.find({}))
    alerts = [{
        'eventType': event_collection.find_one({'id':alert['event_id']})['type'],
        'alerts': event_collection.find_one({'id':alert['event_id']})['alerts_raised'],
        'nodeId': node_collection.find_one({'id':alert['node_id']})['name'],
        'startTime': alert['start_time'],
        'alertTime': alert['alert_time']
    } for alert in alerts if alert["end_time"]==None]
    alerts = alerts[::-1]
    return jsonify(alerts)




@app.route('/data')
def get_data():
   
    total_nodes = node_collection.count_documents({})
    # total_vehicles = instance_collection.count_documents({})
    total_instances = instance_collection.find({})
    total_vehicles, total_potholes, total_parked_vehicles, total_people_count = 0,0,0,0
    for inst in total_instances:
        total_vehicles += inst['vehicle_count']
        total_potholes += inst['pot_hole_count']
        total_parked_vehicles += inst['parked_vehicle_count']
        total_people_count += inst['people_count']


   
    data = {
        'totalNodes': total_nodes,
        'totalVehicles': total_vehicles,
        'totalPotholes': total_potholes,
        'parkedVehicles': total_parked_vehicles,
        'peopleCount': total_people_count
    }
    print(data)
    return jsonify(data)


@app.route('/graph/node', methods=['GET'])
def get_graph():
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
    if timestamps and count:
        sorted_data = sorted(zip(timestamps, count))
        sorted_timestamps, sorted_count = zip(*sorted_data)
    return jsonify({'timestamps': sorted_timestamps, 'count': sorted_count})

@app.route('/graph', methods=['GET'])
def visualize():
    result = node_collection.find({})
    results = []
    for i in result:
        results.append({
            'id': i['id'],
            'name': i['name'],
            'address': i['address'],
        })

    types = ["Parked Vechicle Count", "Vehicle Count", "People Count"]

    return render_template('visualize.html', results=results, types=types)


@app.route('/node/<int:node_id>')
def get_node_data(node_id):
    latest_vehicle = vehicle_collection.find_one({"node_id": node_id}, sort=[("time_stamp", DESCENDING)])
    print(latest_vehicle)
    if latest_vehicle:
        latest_vehicle['_id'] = str(latest_vehicle['_id'])
        if not latest_vehicle.get('car_count'):
            latest_vehicle['car_count'] = 0
        if not latest_vehicle.get('people_count'):
            latest_vehicle['people_count'] = 0
    if latest_vehicle:
        latest_vehicle.update({
            "node_name": node_collection.find_one({"id": node_id})['name']
        })
    
    return jsonify(latest_vehicle)




@app.route('/events/<int:node_id>', methods=['GET'])
def get_events(node_id):
    result = event_collection.find({"node_id": node_id})
    result = list(result)
    result = [{**event, '_id': str(event['_id'])} for event in result]

    return jsonify(result)


@app.route('/instances/<int:node_id>', methods=['GET'])
def get_instances(node_id):
    result = instance_collection.find({"node_id": node_id}, sort=[("time_stamp", DESCENDING)])
    result = list(result)
    result = [{**instance, '_id': str(instance['_id'])} for instance in result]
    return jsonify(result)

@app.route('/alerts/<int:node_id>', methods=['GET', 'POST'])
def get_alerts_specific_node(node_id):
    result = alert_collection.find({"node_id": node_id})
    result = list(result)
    result = [{**alert, '_id': str(alert['_id'])} for alert in result]
    return jsonify(result)


@app.route('/alerts/active/<int:node_id>', methods=['GET', 'POST'])
def get_node_active_alerts(node_id):
    result = event_collection.find({"node_id": node_id})

    result = list(result)
    result = [{**alert, '_id': str(alert['_id'])} for alert in result if alert["end_time"]==None]
    return jsonify(result)


def create_or_update_alert(event_id, node_id, start_time): 
    existing_alert = alert_collection.find_one({"event_id": event_id})
    
    if existing_alert:
        alert_collection.update_one({"event_id": event_id}, {"$set": {"alert_time": datetime.now()}})
    else:
        alert = Alert(event_id, node_id, start_time)
        alert_collection.insert_one(alert.__dict__)


def check_events_for_alerts():
    # return 
    events = event_collection.find({"end_time": None})

    for event in events[:20]:
        start_time = event['start_time']
        alerts_raised = event['alerts_raised']
        current_time = datetime.now()
        
        duration = current_time - start_time
        
        delta = min(4, alerts_raised)

        if delta!=0 and duration > timedelta(minutes=delta*15):
            print(f"Alert: Event duration exceeded {delta*15} minutes")
            create_or_update_alert(event["id"], event["node_id"], event["start_time"])
            event_collection.update_one({"id": event["id"]}, {"$inc": {"alerts_raised": 1}})


scheduler.add_job(check_events_for_alerts, 'interval', minutes=6)
scheduler.start()


if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)