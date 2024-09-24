from NetLogo.ProcessMetadata import NETLOGO_VARIABLES, NETLOGO_REPORTERS

import pynetlogo, json, pandas as pd, geopandas as gpd, logging

# For Mac environments
# netlogo = pynetlogo.NetLogoLink(gui=False)

# For Linux environments


@staticmethod
async def simulate_results(inputParameters):

    netlogo = pynetlogo.NetLogoLink(gui=False, netlogo_home="../../NetLogo 6.3.0")

    netlogo.load_model("./NetLogo/model/Model_Rothenburgsort.nlogo")


    Rothenburgsort = gpd.read_file("./NetLogo/model/data/rothenburgsort.json")

    finalResults = None

    try:
        parameters = {
            NETLOGO_VARIABLES[key]: value for key, value in inputParameters.items()
        }

        logging.debug("Parameters:")
        logging.debug(parameters)

        for key, value in parameters.items():
            # If value is a string, it needs to be wrapped in quotes
            if isinstance(value, str):
                value = f'"{value}"'

            netlogo.command(f"set {key} {value}")

        netlogo.command("setup")

        logging.debug(netlogo)

        results = netlogo.repeat_report(
            list(NETLOGO_REPORTERS.values()),
            parameters["Simulationszeit"] * 12,
            go="go",
        )

        results = pd.DataFrame(results)

        column_rename = {value: key for key, value in NETLOGO_REPORTERS.items()}
        results = results.rename(columns=column_rename)
        results = results.reset_index().rename(columns={"index": "Zeitschritt"})

        simulation_results = pd.DataFrame(results)
        simulation_geometry = Rothenburgsort.geometry.iloc[0]

        finalResults = {
            "simulation_results": simulation_results.to_dict(orient="records"),
            "simulation_geometry": json.loads(simulation_geometry.to_json()),
        }

        finalResults = json.dumps(finalResults)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
       # netlogo.kill_workspace()
        return finalResults
