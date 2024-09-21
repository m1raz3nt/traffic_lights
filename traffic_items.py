import random

class TrafficItem():
    def __init__(self) -> None:
        pass

class Vehicle(TrafficItem):
    def __init__(self) -> None:
        super().__init__()
    
    def is_turn_signal_on(self):
        return random.choice([True, False])

class Pedestrian(TrafficItem):
    def __init__(self) -> None:
        super().__init__()

class TrafficItemBuilder(object):
    def __init__(self) -> None:
        pass

    def build_vehicle(self):
        return Vehicle()
    
    def build_vehicle(self, amount):
        return [Vehicle() for i in range(amount)]

    def build_pedestrian(self):
        return Pedestrian()
    
    def build_pedestrian(self, amount):
        return [Pedestrian() for i in range(amount)]