import socketio
import json

from config import URL, PROCESS_METADATA

from NetLogo.ProcessManager import simulateResults

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

    data.pop("jobID", None)
    inputParameters = data

    print("Input parameters:", inputParameters)


    results = simulateResults(inputParameters)

    print(PROCESS_METADATA)


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
