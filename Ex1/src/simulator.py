from elevator import Elevator
from call import Call


def direction(last_floor, later_floor):
    if int(later_floor[0]) < int(last_floor[0]):
        return -1
    if int(last_floor[0]) > int(last_floor[0]):
        return 1
    return 0


class Simulator:
    def __init__(self, elev: Elevator):
        self.elev = elev
        self.times = {}

    def set_pos(self, c: Call):
        src = str(c.src)
        dest = str(c.dest)
        if len(self.times) == 0:
            self.times[src] = c.time+self.travel_time(0, c.src) + c.time
            self.times[dest] = self.times[src] + self.travel_time(c.src, c.dest) + self.times[src]
        else:
            dict(sorted(self.times.items(), key=lambda item: item[1]))
            it = iter(self.times)
            while it[1] < c.time and it.__next__() is not None:
                it = it.__next__()
            last_floor = it
            if it.__next__() is None:
                self.times[src] = self.travel_time(int(last_floor[0]), c.src) + c.time
                self.times[dest] = self.travel_time(c.src, c.dest) + self.times[src]
            else:
                highest = self.highest_floor()
                lowest = self.lowest_floor()
                src_item = self.insert_src(last_floor, c, highest, lowest)
                dict(sorted(self.times.items(), key=lambda item: item[1]))
                last_floor = iter(self.times)    
                while last_floor.__next__() != src_item:
                    last_floor.__next__()
                self.insert_dest(last_floor, c, highest, lowest)          

    def insert_src(self, last_floor, c, highest, lowest):
        if int(highest[0]) < c.src:
            while last_floor != highest:
                last_floor.__next__()
            src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
            last_floor = last_floor.__next__
        elif int(lowest[0]) > c.src:
            while last_floor != lowest:
                last_floor.__next__()
            src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
            last_floor = last_floor.__next__
        else:
            while last_floor.__next__() is not None:
                if int(last_floor[0]) < c.src < int(last_floor.__next__()[0]) or int(last_floor[0]) > c.src > int(
                        last_floor.__next__()[0]):
                    src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
                    last_floor = last_floor.__next__()
                    break
                last_floor = last_floor.__next__()
        last_floor[1] = src_time + self.travel_time(c.src, int(last_floor[0]))
        while last_floor.__next__() is not None:
            last_floor.__next__()[1] = last_floor[1] + self.travel_time(int(last_floor[0]), int(last_floor.__next__()[0]))
        self.times[str(c.src)] = src_time
        return str(c.src), src_time

    def insert_dest(self, last_floor, c, highest, lowest):
        if int(highest[0]) < c.dest:
            while last_floor != highest:
                last_floor.__next__()
            dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
            last_floor = last_floor.__next__
        elif int(lowest[0]) > c.dest:
            while last_floor != lowest:
                last_floor.__next__()
            dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
            last_floor = last_floor.__next__
        else:
            while last_floor.__next__() is not None:
                if int(last_floor[0]) < c.dest < int(last_floor.__next__()[0]) or int(last_floor[0]) > c.dest > int(
                        last_floor.__next__()[0]):
                    dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
                    last_floor = last_floor.__next__()
                    break
                last_floor = last_floor.__next__()
        last_floor[1] = dest_time + self.travel_time(c.dest, int(last_floor[0]))
        while last_floor.__next__() is not None:
            last_floor.__next__()[1] = last_floor[1] + self.travel_time(int(last_floor[0]),
                                                                        int(last_floor.__next__()[0]))
        self.times[str(c.dest)] = dest_time

    def highest_floor(self):
        max_floor = (str(self.elev.min_floor), 0.0)
        for item in self.times.items():
            if int(item[0]) >= max_floor:
                max_floor = item
        return max_floor

    def lowest_floor(self):
        min_floor = (str(self.elev.max_floor), 0.0)
        for item in self.times.items():
            if int(item[0]) <= min_floor:
                min_floor = item
        return min_floor

    def travel_time(self, src, dest):
        start = self.elev.start_time
        stop = self.elev.stop_time
        open_t = self.elev.open_time
        close_t = self.elev.close_time
        dist = (src + dest) / self.elev.speed
        return ((self.stops(src, dest) + 1) * (start + stop + open_t + close_t)) + dist

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
