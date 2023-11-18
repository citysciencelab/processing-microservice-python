import socketio
import json

from config import URL, PROCESS_METADATA


# SocketIO URL

# Create a SocketIO client
sio = socketio.Client()

# Function to handle SocketIO events
@sio.event
def connect():
    print("SocketIO connection established")

    sio.emit('register', PROCESS_METADATA)

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
