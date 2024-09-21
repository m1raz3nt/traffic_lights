from traffic_light import LightsBuilder

class CrossroadManager():
    def __init__(self, **kwargs) -> None:
        self.lights_builder = LightsBuilder()
        self.vehicle_lights = self.lights_builder.build_vehicle_lights(kwargs.get("vehicle"))
        self.pedestrian_lights = self.lights_builder.build_pedestrian_lights(kwargs.get("pedestrian"))
        
        self.lights_arrangement = []
        # Светофоры можно представить как массив [П, А, П, П, А, П...], где
        # П - пешеходный светофор
        # А - автомобильный светофор
        for i in range(kwargs.get("vehicle")+kwargs.get("pedestrian")):
            if i % 3 == 1:  
                self.lights_arrangement.append(self.vehicle_lights.pop(0))
            else:           
                self.lights_arrangement.append(self.pedestrian_lights.pop(0))

        self.lights_status_map = {tl.id : {"current_state": tl.current_state, "traffic_size": tl.items_queue.qsize()} for tl in self.lights_arrangement}
        self.address_book = {tl.id : tl for tl in self.lights_arrangement}

    # Загруженным светофором считается тот, у которого больше всего предметов в очереди
    def find_jammed_traffic_light(self, recipients):
        queue_sizes = {recipient.get_id() : recipient.get_queue_size() for recipient in recipients}
        return max(queue_sizes, key=queue_sizes.get)

if __name__ == "__main__":
    cm = CrossroadManager(vehicle = 4, pedestrian = 8)
    


    

        
