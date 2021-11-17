import json
from elevator import Elevator


class Building:

    def __init__(self, name_building):
        try:
            with open(name_building, "r") as f:
                # Reading from file
                data = json.loads(f.read())
                self.minFloor = data["_minFloor"]
                self.maxFloor = data["_maxFloor"]
                self.elevators = []
                self.make_elevator(data["_elevators"])
        except FileNotFoundError:
            print("file not found")

    def get_elevator(self, index) -> Elevator:
        """
        return the elevator with the index "index"
        :param index: number of the elevator
        :return: an elevator
        """
        return self.elevators[index]

    def make_elevator(self, elevator_list: list):
        """
        turns a list of dictioneries into a list of elevators
        :param elevator_list: a list of dictioneries
        :return: void
        """
        for i in range(len(elevator_list)):
            d = elevator_list[i]
            self.elevators.append(Elevator(d["_id"], d["_speed"], d["_minFloor"], d["_maxFloor"], d["_closeTime"], d["_openTime"], d["_startTime"], d["_stopTime"]))