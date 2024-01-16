import socketio, json, threading, pandas as pd
from NetLogo.ProcessMetadata import NETLOGO_VARIABLES, NETLOGO_REPORTERS

from importlib import reload
import pynetlogo

from config import URL, PROCESS_METADATA

# Create a SocketIO client
sio = socketio.Client()

jvm_path = None
print("Main class thread ID:", threading.get_ident())


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
    global netlogo
    netlogo = pynetlogo.NetLogoLink(gui=False)
    netlogo.load_model("NetLogo/model/Model_Rothenburgsort.nlogo")

    final_results = None

     # Check if there is data
    if not data:
        print("No data provided - Job", data["jobID"], "aborted")
        return

    # Job ID
    jobID = data["jobID"]

    print("Job execution started (Job ID", jobID, ")")

    data.pop("jobID", None)
    inputParameters = data

    try:
        parameters = {NETLOGO_VARIABLES[key]: value for key, value in inputParameters.items()}

        for key, value in parameters.items():
            # If value is a string, it needs to be wrapped in quotes
            if isinstance(value, str):
                value = f'"{value}"'

            netlogo.command(f'set {key} {value}')

        netlogo.command('setup')

        results = netlogo.repeat_report(NETLOGO_REPORTERS, parameters['Simulationszeit'] * 12, go="go")

        results = pd.DataFrame(results)

        final_results = results.to_json(orient='records')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        print(final_results)
    

    #print("Current thread ID:", threading.get_ident())
    #print("Main thread ID:", threading.main_thread().ident)

    # print("Input parameters:", inputParameters)

    print("JVM path:", jvm_path)

    #results = NetLogo.simulate_results(inputParameters)

    response = {
        "jobID": jobID,
        "processID": PROCESS_METADATA["id"],
        "results": final_results,
        "mimetype": "application/json"
    }

    sio.emit("simulation_results", response)

    print("Job execution finished (Job ID", jobID, ")")

    #jpype.java.lang.Thread.detach()
    netlogo.kill_workspace()

# Function to handle "registration_success" event
@sio.on("registration_success")
def registration_success(data):
    print("registration_success", data)

# Connect to the SocketIO server
if __name__ == "__main__":

    try:
        sio.connect(URL)
        sio.wait()
        
    except Exception as e:
        print("An exception occurred:", str(e))
        # Log the exception here
