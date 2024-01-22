import asyncio
import socketio
from config import URL, PROCESS_METADATA

import NetLogo.ProcessManager as NetLogo
import Mesa.ProcessManager as Mesa

async def main():
    # Create a Socket.IO client instance
    logger = False
    engineio_logger = False

    sio = socketio.AsyncClient(logger=logger, engineio_logger=engineio_logger)

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

        print("Job execution started (Job ID", jobID, ")")

        data.pop("jobID", None)
        inputParameters = data        

        # print("Input parameters:", inputParameters)

        results = await NetLogo.simulate_results(inputParameters)

        response = {
            "jobID": jobID,
            "processID": PROCESS_METADATA["id"],
            "results": results,
            "mimetype": "application/json"
        }

        await sio.emit("simulation_results", response)

        print("Job execution finished (Job ID", jobID, ")")

    # Connect to the server
    await sio.connect(URL)

    # Wait for the connection to be established
    await sio.wait()

# Run the main function
asyncio.run(main())
