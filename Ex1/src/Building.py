import json
import Elevator
class Building:
    _minFloor = 0
    _maxFloor = 0
    _elevators = []

    def __init__(self, name_Building):
        f = open(name_Building, "r")

        # Reading from file
        data = json.loads(f.read())
        _minFloor = data["_minFloor"]
        _maxFloor = data["_maxFloor"]
        self.makeElevator(data["_elevators"])

    def getElevator(self, index):
        return self._elevators[index]

    def makeElevator(self,elevatorlist):
        for i in range(len(elevatorlist)):
            d=elevatorlist[i]
            self._elevators[i]=Elevator(d["_id"],["_speed"],["_minFloor"],["_maxFloor"],["_closeTime"],["_openTime"],["_startTime"],["_stopTime"])
