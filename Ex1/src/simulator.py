from elevator import Elevator
from call import Call


class Simulator:
    # this class was made to simulate in what time the elevator is at any of the floors it's allocated to
    def __init__(self, elev: Elevator):
        self.elev = elev
        self.times = {}

    def set_pos(self, c: Call):
        """
        insert the dest and src floors of the call c to the times dictionary
        and update the times of all the other floors accordingly
        :param c: call allocated to this elevator
        :return: None
        """
        src = str(c.src)
        dest = str(c.dest)
        if len(self.times) == 0:  # first call
            self.times[src] = c.time+self.travel_time(0, c.src) + c.time
            self.times[dest] = self.times[src] + self.travel_time(c.src, c.dest) + self.times[src]
        else:
            dict(sorted(self.times.items(), key=lambda item: item[1]))
            it = iter(self.times)
            while it[1] < c.time and it.__next__() is not None:
                it = it.__next__()
            last_floor = it
            if it.__next__() is None:  # this call is recived after all the others are finished
                self.times[src] = self.travel_time(int(last_floor[0]), c.src) + c.time
                self.times[dest] = self.travel_time(c.src, c.dest) + self.times[src]
            else:  # insert this call in the middle
                highest = self.highest_floor()
                lowest = self.lowest_floor()
                src_item = self.insert_src(last_floor, c, highest, lowest)
                dict(sorted(self.times.items(), key=lambda item: item[1]))
                last_floor = iter(self.times)
                while last_floor.__next__() != src_item:
                    last_floor.__next__()
                self.insert_dest(last_floor, c, highest, lowest)

    def insert_src(self, last_floor, c, highest, lowest):
        """
        insert the src floor with the time that the elevator would get to it to the times dictionary
        :param last_floor: iterator on the times dict
        :param c: the call allocated to this elevator
        :param highest: highest floor in times
        :param lowest: lowest floor in times
        :return: tuple
        """
        src_time = 0
        if int(highest[0]) < c.src:  # if c.src is the highest floor in times
            while last_floor != highest:
                last_floor.__next__()
            src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
            last_floor = last_floor.__next__
        elif int(lowest[0]) > c.src:  # if c.src is the lowest floor in times
            while last_floor != lowest:
                last_floor.__next__()
            src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
            last_floor = last_floor.__next__
        else:  # c.src is between two floors
            while last_floor.__next__() is not None:
                if int(last_floor[0]) < c.src < int(last_floor.__next__()[0]) or int(last_floor[0]) > c.src > int(
                        last_floor.__next__()[0]):
                    src_time = self.travel_time(int(last_floor[0]), c.src) + last_floor[1]
                    last_floor = last_floor.__next__()
                    break
                last_floor = last_floor.__next__()
        last_floor[1] = src_time + self.travel_time(c.src, int(last_floor[0]))
        while last_floor.__next__() is not None:  # update the times of the later floors
            last_floor.__next__()[1] = last_floor[1] + self.travel_time(int(last_floor[0]), int(last_floor.__next__()[0]))
        self.times[str(c.src)] = src_time
        tup = (str(c.src), src_time)
        return tup

    def insert_dest(self, last_floor, c, highest, lowest):
        """
        insert the dest floor with the time that the elevator would get to it to the times dictionary
        :param last_floor: iterator on the times dict
        :param c: the call allocated to this elevator
        :param highest: highest floor in times
        :param lowest: lowest floor in times
        :return: None
        """
        dest_time = 0
        if int(highest[0]) < c.dest:  # if c.dest is the highest floor in times
            while last_floor != highest:
                last_floor.__next__()
            dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
            last_floor = last_floor.__next__
        elif int(lowest[0]) > c.dest:  # if c.dest is the lowest floor in times
            while last_floor != lowest:
                last_floor.__next__()
            dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
            last_floor = last_floor.__next__
        else:  # c.dest is between floors
            while last_floor.__next__() is not None:
                if int(last_floor[0]) < c.dest < int(last_floor.__next__()[0]) or int(last_floor[0]) > c.dest > int(
                        last_floor.__next__()[0]):
                    dest_time = self.travel_time(int(last_floor[0]), c.dest) + last_floor[1]
                    last_floor = last_floor.__next__()
                    break
                last_floor = last_floor.__next__()
        last_floor[1] = dest_time + self.travel_time(c.dest, int(last_floor[0]))
        while last_floor.__next__() is not None:  # update the times of the later floors
            last_floor.__next__()[1] = last_floor[1] + self.travel_time(int(last_floor[0]),
                                                                        int(last_floor.__next__()[0]))
        self.times[str(c.dest)] = dest_time

    def highest_floor(self):
        """
        find the highest floor in times
        :return: highest floor
        """
        max_floor = (str(self.elev.min_floor), 0.0)
        for item in self.times.items():
            if int(item[0]) >= max_floor:
                max_floor = item
        return max_floor

    def lowest_floor(self):
        """
        find the lowest floor in times
        :return: lowest floor
        """
        min_floor = (str(self.elev.max_floor), 0.0)
        for item in self.times.items():
            if int(item[0]) <= min_floor:
                min_floor = item
        return min_floor

    def travel_time(self, src, dest):
        """
        calculate travel time between two floors
        :param src: the source floor
        :param dest: the destination floor
        :return: the calculated travel time
        """
        start = self.elev.start_time
        stop = self.elev.stop_time
        open_t = self.elev.open_time
        close_t = self.elev.close_time
        dist = (src + dest) / self.elev.speed
        return start + stop + open_t + close_t + dist

