from NetLogo.ProcessMetadata import NETLOGO_VARIABLES, NETLOGO_REPORTERS
from importlib import reload

import pynetlogo, pandas as pd

netlogo = pynetlogo.NetLogoLink(gui=False)
netlogo.load_model("./NetLogo/model/Model_Rothenburgsort.nlogo")

async def simulate_results(inputParameters):

    # For Linux environments
    # netlogo = pynetlogo.NetLogoLink(gui=False, netlogo_home='../../NetLogo 6.3.0')

    # For Mac environments
    # netlogo = pynetlogo.NetLogoLink(gui=False, jvm_path=jvm_path)

    netlogo.load_model("./NetLogo/model/Model_Rothenburgsort.nlogo")

    finalResults = None

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

        finalResults = results.to_json(orient='records')
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        netlogo.kill_workspace()

        return finalResults
