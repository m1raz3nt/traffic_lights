import queue
from uuid import uuid4


# У каждого светофора есть свой id, id светофора с противоположной стороны и очередь авто/пешеходов
# Хорошей идеей кажется назначение левого и правого соседа светофору
class TrafficLight:
    def __init__(self):

        self.id = uuid4()
        self.type = "basic"

        self.traffic_items_queue = queue.Queue()
        self.events_queue = queue.Queue()
        self.timer_cutoff = 0

        self.current_state = None

        self.left_neighbor = None
        self.right_neighbor = None

    def get_current_state(self):
        return self.current_state

    # def generate_event(self, state_to_switch, timer_cutoff):
    #     # TODO: Это стоит записать в логгер
    #     event = {
    #         "sender_id": self.id,
    #         "sender_type": self.type,
    #         "sender_switched_from": self.current_state,
    #         "sender_switches_to": state_to_switch,
    #         "sender_switches_in": timer_cutoff
    #     }
    #     return event

    def generate_event(self, recipient, state_to_switch):
        pass
    
    def place_event(self, report):
        self.events_queue.put(report)

# Для автомобильных светофоров хорошей идеей будет назначить автомобильный сфетофор слева
# Как еще одного соседа (для функционала желтого света)
class VehicleLight(TrafficLight):
    def __init__(self) -> None:
        super().__init__()
        self.type = "vehicle"
        self.corresponding_vehicle_light = None

    def process_events_queue(self):
        # Забираем верхний ивент с очереди
        current_report = self.events_queue.get()
        # У автомобильного светофора соседями являются только пешеходные светофоры
        # Если переключился левый сосед
        if current_report.get("sender_id") == self.right_neighbor.id:
            # Выставляем жетый свет на время 
            self.current_state = "yellow"
            # time.sleep(current_report.get("timer_cutoff"))
            # После чего снижаем очередь у соседнего автомобильного светофора
            self.corresponding_vehicle_light.traffic_items_queue.pop()

class PedestrianLight(TrafficLight):
    def __init__(self) -> None:
        super().__init__()
        self.type = "pedestrian"
        self.color_counterparts = {
            "red": "green",
            "green": "red",
            "yellow": "red"
        }
    
    def process_events_queue(self):
        # Забираем верхний ивент с очереди
        current_report = self.events_queue.get()
        # Если переключился сосед - пешеходный светофор
        if current_report.get("sender_id") == self.right_neighbor.id or current_report.get("sender_id") == self.left_neighbor.id:
            if current_report.get("sender_type") == "pedestrian":
                # То меняем цвет на противоположный c задержкой таймера
                # time.sleep(current_report.get("timer_cutoff"))
                self.current_state = self.color_counterparts.get(current_report.get("sender_switches_to"))

        # Если переключился сосед - автомобильный светофор
        if current_report.get("sender_id") == self.right_neighbor.id or current_report.get("sender_id") == self.left_neighbor.id:
            if current_report.get("sender_type") == "vehicle":
                # То меняем цвет на противоположный c задержкой таймера
                # time.sleep(current_report.get("timer_cutoff"))
                self.current_state = self.color_counterparts.get(current_report.get("sender_switches_to"))
        
        # Если светофор дал зеленый свет, то снижаем очередь на 1
        # TODO: Надо записать в логгер
        if self.current_state == "green":
            self.traffic_items_queue.pop()
        
        # В зависимости от положения отправителя отправляем запрос дальше
        if current_report.get("sender_id") == self.right_neighbor.id:
            self.generate_event(self.left_neighbor, self.current_state)
        if current_report.get("sender_id") == self.left_neighbor.id:
            self.generate_event(self.right_neighbor, self.current_state)


# Можно ли это назвать Фабрикой? Я не уверен.
class LightsBuilder(object):
    def __init__(self) -> None:
        pass

    def build_vehicle_light(self):
        return VehicleLight()
    
    def build_vehicle_lights(self, amount):
        return [VehicleLight() for i in range(amount)]

    def build_pedestrian_light(self):
        return PedestrianLight()
    
    def build_pedestrian_lights(self, amount):
        return [PedestrianLight() for i in range(amount)]

