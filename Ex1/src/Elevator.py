

class Elevator:

    def __init__(self, _id, speed, min_floor, max_floor, close_time, open_time, star_time, stop_time):
        self.id = _id
        self.speed = speed
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.close_time = close_time
        self.open_time = open_time
        self.start_time = star_time
        self.stop_time = stop_time
        self.calls = []

    def add_call(self, call):
        """
        add call to the call list
        :param call: a call allocated to self
        :return: void
        """
        self.calls.append(call)
