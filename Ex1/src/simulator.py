from elevator import Elevator
from call import Call


def direction(last_floor, later_floor):
    if int(later_floor[0]) < int(last_floor[0]):
        return -1
    if int(last_floor[0]) > int(last_floor[0]):
        return 1
    return 0


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
            dict(sorted(self.times.items(), key=lambda item: item[1]))
            it = iter(self.times)
            while it[1] < c.time and it.__next__() is not None:
                it.__next__()
            last_floor = it
            if it.__next__() is None:
                self.times[src] = self.travel_time(int(last_floor[0]), c.src)
                self.times[dest] = self.travel_time(c.src, c.dest)
            else:
                later_floor = it.__next__()
                curr_direct = direction(last_floor, later_floor)
                # complete the case that the call is in the middle

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
