import pandas as pd, geopandas as gpd
from Mesa.model.model import RobotModel


async def simulate_results(inputParameters):

    finalResults = None

    try:
        robot_model = RobotModel(number_of_robots=inputParameters["number-of-robots"])
                           
        for i in range(inputParameters["simulation-time"]):
            robot_model.step()

        results = robot_model.datacollector.get_agent_vars_dataframe()
        results = results.reset_index().rename(columns={"index": "Zeitschritt"})

        rgpd = gpd.GeoDataFrame(results, geometry="geometry")

        finalResults = rgpd[["Speed", "Info", "geometry"]].to_json()
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        return finalResults