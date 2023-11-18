import socketio
import json

from config import URL, PROCESS_METADATA


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


# Function to handle "execute" event
@sio.event
def execute(data):

    print(data)

    # Check if there is data
    if not data:
        print("No data provided - Job", data["jobID"], "aborted")
        return

    # Job ID
    jobID = data["jobID"]

    print("Job execution started (Job ID", jobID, ")")

    # Input parameters
    inputParameters = {}

    # Iterate over the input parameters and rename the keys
    for key, value in data.items():
        # Skip the jobID
        if key == "jobID":
            continue

        try:
            title = PROCESS_METADATA["inputs"][key]["title"]
            inputParameters[title] = value
        except KeyError:
            continue

    # simulateResults function
    def simulateResults(inputParameters):
        # Your implementation of simulateResults function goes here
        pass

    results = simulateResults(inputParameters)

    response = {
        "jobID": jobID,
        "processID": PROCESS_METADATA["id"],
        "results": results,
        "mimetype": "application/json"
    }

    sio.emit("simulation_results", response)

    print("Job execution finished (Job ID", jobID, ")")

# Function to handle "registration_success" event
@sio.on("registration_success")
def registration_success(data):
    print("registration_success", data)


# Connect to the SocketIO server
if __name__ == "__main__":
    sio.connect(URL)
    sio.wait()
