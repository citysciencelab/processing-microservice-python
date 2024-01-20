import mesa, mesa_geo as mg, math, geopandas as gpd, random, requests, pyproj
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import transform

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

# Functions
def generate_random_point_in_polygon(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    while True:
        pnt = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(pnt):
            return pnt
        
to_meters = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:4326'),
    pyproj.Proj(init='epsg:25832')) 

to_wgs = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:25832'),
    pyproj.Proj(init='epsg:4326'))

# Classes
class Stadtteil(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs):
        super().__init__(unique_id, model, geometry, crs)


class Tree(mg.GeoAgent):
    def __init__(self, unique_id, model, geometry, crs, state="healthy", planting_step=0):
        super().__init__(unique_id, model, geometry, crs)
        self.state = state
        self.planting_step = planting_step
        print("Tree planted at step " + str(self.planting_step))
    
    def update_with_interaction(self, action):
        print(action)
        
        if action == "Destroyed":
            self.state = "destroyed"
            self.info = "I was destroyed"
        
        elif action == "Watered":
            self.state = "Moving"
            self.info = "I was watered at simulation step " + str(self.model.schedule.steps)


class Robot(mg.GeoAgent):

    tree_planting_time = 60 # seconds

    def __init__(self, unique_id, model, geometry, crs, speed=15, direction=None, destination=None, state="Moving"):
        super().__init__(unique_id, model, geometry, crs)
        self.direction = direction
        self.direction_meters = LineString([(0, 0), (0,0)]) # Initial zero line
        self.speed = speed # Unit: meters per step
        self.destination = destination
        self.distance_travelled = 0
        self.info = ""
        self.state = state
        self.tree_planting_time_elapsed = 0

    def step(self):
        
        # Don't do anything, if state is destroyed
        if self.state == "Destroyed":
            return
        
        # Vary speed randomly
        self.speed = max(0, self.speed + self.random.uniform(-5, 5))

        # See if we are at the destination
        if self.destination is not None:
            self.info = "I have a destination"
            # If we are, stop moving
            if self.distance_travelled > 0 and self.distance_travelled >= self.direction_meters.length:
                
                self.info = "I am at my destination"
                self.state = "Planting"

                # Start planting timer
                self.tree_planting_time_elapsed += self.model.time_between_steps

                # If the timer is up, plant a tree
                if self.tree_planting_time_elapsed >= self.tree_planting_time:
                    self.destination = None
                    self.distance_travelled = 0
                    
                    self.plant_tree()
                    self.tree_planting_time_elapsed = 0
                    self.state = "Moving"
                
            # If not, move towards it
            else:
                self.move_towards_destination()
        
        # If there is no destination, pick one
        else:
            self.info = "Looking for a destination"
            self.get_new_destination()

    def move_towards_destination(self):

        self.distance_travelled += self.speed
        self.geometry = transform(to_wgs.transform, self.direction_meters.interpolate(self.distance_travelled))

    def get_new_destination(self):
        
        ceiled_place = self.model.ceiled_places.sample(1).iloc[0]
        self.destination = ceiled_place.geometry.centroid

        # Get routing to area
        self.get_routing()

    def get_routing(self):
        
        # URL for the routing service
        url = "https://ors.comaps.eu/ors/v2/directions/cycling-regular?start=" + str(self.geometry.x) + "," + str(self.geometry.y) + "&end=" + str(self.destination.x) + "," + str(self.destination.y)

        # Request the route
        r = requests.get(url, verify=False)

        # Try to parse the route
        try:
            route = r.json()["features"][0]["geometry"]
            self.direction = LineString(route["coordinates"])
            self.direction_meters = transform(to_meters.transform, self.direction)
            self.info = "I have a route"
        
        # If it fails, get another destination
        except:
            self.info = "I could not get a route"

    def plant_tree(self):
        self.model.space.add_agents([Tree(self.unique_id + "-tree-" + str(self.model.schedule.steps), self.model, self.geometry, self.crs, planting_step=self.model.schedule.steps)])

    def update_with_interaction(self, action):
        
        if action == "Destroyed":
            self.state = "Destroyed"
            self.info = "I was destroyed"
        
        elif action == "Repaired":
            self.state = "Moving"
            self.info = "I was repaired"