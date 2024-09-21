from typing import List
import traffic_items
from traffic_light import LightsBuilder

# На перекрестке 12 светофоров:
# 4 для автомобилей и 8 для пешеходов

class Crossroad():
    def __init__(self, **lights_config) -> None:
        self.lights_builder = LightsBuilder()
        self.traffic_lights = []
        self.set_lights(lights_config)

        self.population = []

    # Этим методом можно населить перекресток
    def populate_crossroad(self, vehicle_count, pedestrian_count) -> None:
        self.population.extend(vehicle_count*[traffic_items.Vehicle()])
        self.population.extend(pedestrian_count*[traffic_items.Pedestrian()])

    def set_lights(self, lights_config):
        self.traffic_lights.extend(self.lights_builder.build_vehicle_lights(lights_config.get("vehicle")))
        self.traffic_lights.extend(self.lights_builder.build_pedestrian_lights(lights_config.get("pedestrian")))
