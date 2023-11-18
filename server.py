import socketio
import json

# SocketIO URL
URL = 'http://localhost:5555'

# Create a SocketIO client
sio = socketio.Client()

# Function to handle SocketIO events
@sio.event
def connect():
    print("SocketIO connection established")
    # Send the registration event
    register_event = {
        'event': 'register',
        'data': {
            'version': '0.1.0',
            'id': 'tree-planting-robots',
            'title': {'en': 'CCmCC Tree planting robot Model'},
            'description': {'en': 'This is the Mesa-geo model for the CCmCC project tree planting robots'},
            'jobControlOptions': ['sync-execute', 'async-execute'],
            'links': [{'type': 'text/html', 'rel': 'about', 'title': 'information', 'href': 'http://...'}]
        }
    }
    sio.emit('register', json.dumps(register_event))

@sio.event
def disconnect():
    print("SocketIO connection closed")

@sio.event
def message(data):
    data = json.loads(data)
    event = data.get('event')
    if event == 'register':
        handle_register(data)
    elif event == 'simulation_results':
        handle_simulation_results(data)

def handle_register(data):
    print("Registered successfully")

def handle_simulation_results(data):
    result = data.get('result')
    print("Simulation results:", result)

# Connect to the SocketIO server
if __name__ == "__main__":
    sio.connect(URL)
    sio.wait()
