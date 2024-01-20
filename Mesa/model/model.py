import warnings
warnings.filterwarnings("ignore")

import requests, json, time

import mesa, os, mesa_geo as mg, geopandas as gpd, math, random
from shapely.geometry import Point

# Set to current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from agents import *

# Config for Database
#url = "http://localhost:3000" #url of the api
url = "https://robotapi.cut.hcu-hamburg.de"

# Config for Simulation
time_between_steps = 5 #seconds

# Load Data
stadtteile = gpd.read_file('data/bevoelkerung_stadtteile.json') #district tile

#bodenversiegelung = gpd.read_file('data/bodenversiegelung.json') #floor sealing
#ceiled_places = bodenversiegelung[bodenversiegelung["versiegelungsklasse"] > 6]

ceiled_places = gpd.read_file('data/ceiled_places_without_trees.geojson') #floor sealing

baumschulen = [
    {
        "name": "Baumschule Lorenz von Ehren",
        "location": Point(9.9364, 53.4289)
    },
    {
        "name": "Gärtnerei Lohbrügge",
        "location": Point(10.2056, 53.5131)
    },
    {
        "name": "Baumschule Finkenwerder",
        "location": Point(9.8714, 53.5269)
    },
]


# Generate a random simulation hash
simulation_hash = ''.join(random.choice('0123456789ABCDEF') for i in range(16))


def generate_random_point_in_polygon(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    while True:
        pnt = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(pnt):
            return pnt

        
class RobotModel(mesa.Model):

    def __init__(self, number_of_robots = 5):
        self.space = mg.GeoSpace(crs="epsg:4326") #mesa setting - projection setting 
        self.schedule = mesa.time.RandomActivation(self) #random each order step
        self.running = True 

        # Data shared across the model
        self.ceiled_places = ceiled_places
        self.time_between_steps = time_between_steps
        self.last_step = time.time()

        ac = mg.AgentCreator(agent_class=Stadtteil, model=self) #district agent
        agents = ac.from_GeoDataFrame(gdf=stadtteile, unique_id="stadtteil")
        self.space.add_agents(agents)

        self.space.add_agents([Tree("EternalTree",  model=self, geometry=Point(10.0014,53.5422), crs="epsg:4326")])

        ac = mg.AgentCreator(agent_class=Robot, model=self,crs="epsg:4326") #robots

        # for stadtteil in stadtteile["stadtteil"]:

        #     #create five robots per Stadtteil

        #     for i in range(number_of_robots):
        #         location = generate_random_point_in_polygon(stadtteile[stadtteile["stadtteil"] == stadtteil]["geometry"].values[0])
        #         agent = ac.create_agent(location, stadtteil + "-" + str(i))
        #         agent.ceiled_places = ceiled_places
        #         self.space.add_agents([agent])
        #         self.schedule.add(agent)

        for i in range(number_of_robots):
            # Select a random Baumschule
            baumschule = baumschulen[random.randint(0, len(baumschulen) - 1)]
            robot = Robot("Robot-" + str(i),  model=self, geometry=baumschule["location"], crs="epsg:4326")
            self.space.add_agents([robot])
            self.schedule.add(robot)
            
        self.datacollector = mesa.DataCollector(
            model_reporters={}, agent_reporters={"geometry": "geometry", "Speed": "speed", "Info": "info", "Destination": "destination"}
        )

        # @property
        # def dataAtTime(self):
        #     print(self._DATA)

    def step(self):
        
        self.last_step = time.time()
        self.datacollector.collect(self)

        #self.update_with_interaction_data()

        self.schedule.step()
        #self.write_to_database()

        #while time.time() - self.last_step < time_between_steps:
        #    time.sleep(1)

    
    
    def write_to_database(self):

        # Get tree and robot data
        robot_agents = self.get_robot_data()
        tree_agents = self.get_tree_data()
        

        agents = {
            "robots": robot_agents,
            "trees": tree_agents,
        }


        # Write to database
        res = requests.post(url + "/simulation-step", json=agents)

        # Print response if status code is not 200
        if res.status_code != 201:
            print(res.text)
    
    def get_robot_data(self):
        robot_agents = self.space.get_agents_as_GeoDataFrame(agent_cls=Robot)
        robot_agents.reset_index(inplace=True)
        robot_agents.rename(columns={'unique_id': 'name', 'geometry': 'location', 'direction': 'current_route'}, inplace=True)
        robot_agents['simulation_step'] = self.schedule.steps
        robot_agents = robot_agents[['name', 'info', 'location', 'current_route', 'speed', 'simulation_step']]
        robot_agents['location'] = robot_agents['location'].apply(lambda p: p.__geo_interface__ if p is not None else None) # Turn location into a geojson object   
        robot_agents['current_route'] = robot_agents['current_route'].apply(lambda p: p.__geo_interface__ if p is not None else None)

        return robot_agents.to_dict(orient='records')
    
    def get_tree_data(self):
        tree_agents = self.space.get_agents_as_GeoDataFrame(agent_cls=Tree)
        
        tree_agents = tree_agents[tree_agents["planting_step"] == (self.schedule.steps - 1)] # Only add those that were planted this step

        tree_agents.reset_index(inplace=True)
        tree_agents.rename(columns={'unique_id': 'name', 'geometry': 'location', 'state':'status', 'planting_step':'simulation_step_planted'}, inplace=True)
        tree_agents['location'] = tree_agents['location'].apply(lambda p: p.__geo_interface__ if p is not None else None) # Turn location into a geojson object

        return tree_agents.to_dict(orient='records')
    
    def update_with_interaction_data(self):
        # Get interaction data from API
        res = requests.get(url + "/interactions")

        robots = {}
        trees = {}
        updates_processed = []

        # If status code is 200, update the model
        if res.status_code == 200:
            data = res.json()

            if len(data) == 0:
                return

            # Iterate over all interactions
            for interaction in data:
                # If the interaction is a robot, add it to the robot dict
                if interaction["type"] == "robot":
                    robots[interaction["unique_id"]] = interaction
                
                # If the interaction is a tree, add it to the tree dict
                elif interaction["type"] == "tree":
                    trees[interaction["unique_id"]] = interaction
                
                # Add the interaction to the processed list
                updates_processed.append(interaction["id"])

            # Iterate over all agents
            for agent in self.space.agents:
                # If the agent is a robot, update it with the robot dict
                if isinstance(agent, Robot):
                    if agent.unique_id in robots:
                        agent.update_with_interaction(robots[agent.unique_id]["action"])
                
                # If the agent is a tree, update it with the tree dict
                elif isinstance(agent, Tree):
                    if agent.unique_id in trees:
                        agent.update_with_interaction(trees[agent.unique_id]["action"])

            updates_processed = {"interactionUpdates": updates_processed, "newInteractions" : []}

            # Post all interactions as processed
            res = requests.post(url + "/interactions", json=updates_processed)

            # Print response if status code is not 200
            if res.status_code != 201:
                print(res.text)
            

            


           

    


