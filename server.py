import asyncio, socketio, logging
from config import URL, PROCESS_METADATA

import NetLogo.ProcessManager as NetLogo
#import Mesa.ProcessManager as Mesa

logger = True
engineio_logger = True
logging.basicConfig(level=logging.DEBUG)

sio = socketio.AsyncClient(logger=logger, engineio_logger=engineio_logger)

async def main():
    # Create a Socket.IO client instance
    # Connect to the server
    await sio.connect(URL)

    # Wait for the connection to be established
    await sio.wait()

# Define event handlers
@sio.event
async def connect():
    print('Connected to server')
    await sio.emit('register', PROCESS_METADATA)

@sio.event
async def disconnect():
    print('Disconnected from server')


@sio.on("registration_success")
def registration_success(data):
    print("registration_success", data)


# Function to handle "execute" event
@sio.event
async def execute(data):

    # Check if there is data
    if not data:
        print("No data provided - Job", data["jobID"], "aborted")
        return

    # Job ID
    jobID = data["jobID"]

    logging.debug("Job execution started")
    logging.debug(jobID)

    data.pop("jobID", None)
    inputParameters = data        

    # print("Input parameters:", inputParameters)
    results = "Dummy results"

    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(NetLogo.simulate_results(inputParameters))
        logging.debug("Task created")
        logging.debug(task)
        results = await task
        logging.debug("Results:")
        logging.debug(results)
    except Exception as e:
        logging.error(f"An error occurred while simulating results: {e}")
        results = None

    response = {
        "jobID": jobID,
        "processID": PROCESS_METADATA["id"],
        "results": results,
        "mimetype": "application/json"
    }

    await sio.emit("simulation_results", response)

    print("Job execution finished (Job ID", jobID, ")")


# Run the main function
# Start the main function
if __name__ == "__main__":
    asyncio.run(main())
