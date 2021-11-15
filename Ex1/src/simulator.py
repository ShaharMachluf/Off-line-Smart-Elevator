from elevator import Elevator
from call import Call


class Simulator:
    def __init__(self, elev: Elevator, time: float):
        self.elev = elev
        self.time = time
        self.times = {}

    def set_pos(self, c: Call):
        src = str(c.src)
        dest = str(c.dest)
        if len(self.times) == 0:
            self.times[src] = c.time+self.travel_time(0, c.src)
            self.times[dest] = self.times[src] + self.travel_time(c.src, c.dest)
        else:
            last_floor = (0, 0)
            count = 0
            for item in self.times.items():
                if last_floor[1] < item[1] <= c.time:
                    last_floor = (int(item[0]), item[1])
                    count += 1
            if count == len(self.times):



    def direction(self, last_floor):
        min_time = (0, 0)
        for item in self.times.items():
            if min_time[1] > item[1] > last_floor[1]:
                min_time = (int(item[0]), item[1])
        if min_time[0]<last_floor[0]:
            return  -1
        if min_time[0]>last_floor[0]:
            return 1
        return 0

    def travel_time(self, src, dest):
        start = self.elev.start_time
        stop = self.elev.stop_time
        open_t = self.elev.open_time
        close_t = self.elev.close_time
        dist = (src+dest)/self.elev.speed
        return (self.stops(src, dest) * (start+stop+open_t+close_t)) + dist

    def stops(self, src, dest):
        count = 0
        if src < dest and len(self.elev.calls) > 0:
            i = 0
            c = self.elev.calls[i]
            while c.dest <= dest or c.src <= dest:
                if src <= c.dest < dest:
                    count = count + 1
                if src <= c.src < dest:
                    count = count + 1
                i += 1
                c = self.elev.calls[i]
        else:
            if len(self.elev.calls) > 0:
                i = 0
                c = self.elev.calls[i]
                while c.dest >= dest or c.src >= dest:
                    if src >= c.dest > dest:
                        count = count + 1
                    if src >= c.src > dest:
                        count = count + 1
                    i += 1
                    c = self.elev.calls[i]
        return count
