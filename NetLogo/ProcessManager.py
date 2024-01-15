import pynetlogo, pandas as pd, geopandas as gpd
from NetLogo.ProcessMetadata import NETLOGO_VARIABLES, NETLOGO_REPORTERS

# For Linux environments
# netlogo = pynetlogo.NetLogoLink(gui=False, netlogo_home='../../NetLogo 6.3.0')

# For Mac environments
netlogo = pynetlogo.NetLogoLink(gui=False)

netlogo.load_model("./NetLogo/model/Model_Rothenburgsort.nlogo")


def simulateResults(inputParameters):

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

        return results.to_json(orient='records')
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
