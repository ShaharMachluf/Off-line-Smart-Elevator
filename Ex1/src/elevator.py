from call import Call


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
        self.times = {}

    def add_call(self, call):
        """
        add call to the call list
        :param call: a call allocated to self
        :return: void
        """
        self.calls.append(call)

    def set_pos(self, c: Call):
        """
        insert the dest and src floors of the call c to the times dictionary
        and update the times of all the other floors accordingly
        :param c: call allocated to this elevator
        :return: None
        """
        if len(self.times) == 0:  # first call
            src_time = c.time + self.travel_time(0, c.src) + c.time
            dest_time = src_time + self.travel_time(c.src, c.dest) + src_time
            self.times[str(src_time)] = c.src
            self.times[str(dest_time)] = c.dest
        else:
            dict(sorted(self.times.items(), key=lambda item: item[0]))
            k_list = list(self.times.keys())
            i = 0
            while float(k_list[i]) < c.time and i < len(k_list)-1:
                i += 1
            last_floor = self.times[k_list[i]]
            if i == len(k_list):  # this call is recived after all the others are finished
                src_time = self.travel_time(last_floor, c.src) + c.time
                dest_time = self.travel_time(c.src, c.dest) + src_time
                self.times[str(src_time)] = c.src
                self.times[str(dest_time)] = c.dest
            else:  # insert this call in the middle
                highest = self.highest_floor()
                lowest = self.lowest_floor()
                src_item = self.insert_src(k_list, i, c, highest, lowest)
                dict(sorted(self.times.items(), key=lambda item: float(item[0])))
                k_list = list(self.times.keys())
                i = 0
                while float(k_list[i]) != float(src_item[0]):
                    i += 1
                self.insert_dest(k_list, i, c, highest, lowest)

    def insert_src(self, k_list: list, i, c, highest, lowest):
        """
        insert the src floor with the time that the elevator would get to it to the times dictionary
        :param i: index
        :param k_list: list of keys (times)
        :param c: the call allocated to this elevator
        :param highest: highest floor in times
        :param lowest: lowest floor in times
        :return: tuple
        """
        src_time = 0
        if highest < c.src:  # if c.src is the highest floor in times
            while self.times[k_list[i]] != highest:
                i += 1
            src_time = self.travel_time(self.times[k_list[i]], c.src) + float(k_list[i])
            i += 1
        elif lowest > c.src:  # if c.src is the lowest floor in times
            while self.times[k_list[i]] != lowest:
                i += 1
            src_time = self.travel_time(self.times[k_list[i]], c.src) + float(k_list[i])
            i += 1
        else:  # c.src is between two floors
            while i < len(k_list)-1:
                if self.times[k_list[i]] <= c.src < self.times[k_list[i+1]] or self.times[k_list[i]] >= c.src > self.times[k_list[i+1]]:
                    src_time = self.travel_time(self.times[k_list[i]], c.src) + float(k_list[i])
                    i += 1
                    break
                i += 1
        x=str(src_time + self.travel_time(c.src, self.times[k_list[i]]))
        self.times[x] = self.times[k_list[i]]
        self.times.pop(k_list[i])
        k_list[i] = x
        i += 1
        while i < len(k_list)-1:  # update the times of the later floors
            x=str(float(k_list[i]) + self.travel_time(self.times[k_list[i]], self.times[k_list[i+1]]))
            self.times[x] = self.times[k_list[i+1]]
            self.times.pop(k_list[i+1])
            k_list[i + 1] = x
            i += 1
        self.times[str(src_time)] = c.src
        tup = (str(src_time), c.src)
        return tup

    def insert_dest(self, k_list: list, i, c, highest, lowest):
        """
        insert the dest floor with the time that the elevator would get to it to the times dictionary
        :param i: index
        :param k_list: list of keys (times)
        :param c: the call allocated to this elevator
        :param highest: highest floor in times
        :param lowest: lowest floor in times
        :return: None
        """
        dest_time = 0
        if highest < c.dest:  # if c.dest is the highest floor in times
            while self.times[k_list[i]] != highest:
                i += 1
            dest_time = self.travel_time(self.times[k_list[i]], c.dest) + float(k_list[i])
            i += 1
        elif lowest > c.dest:  # if c.dest is the lowest floor in times
            while self.times[k_list[i]] != lowest:
                i += 1
            dest_time = self.travel_time(self.times[k_list[i]], c.dest) + float(k_list[i])
            i += 1
        else:  # c.dest is between floors
            while i < len(k_list)-1:
                if self.times[k_list[i]] <= c.dest < self.times[k_list[i+1]] or self.times[k_list[i]] >= c.dest > self.times[k_list[i+1]]:
                    dest_time = self.travel_time(self.times[k_list[i]], c.dest) + float(k_list[i])
                    i += 1
                    break
                i += 1
        x = str(dest_time + self.travel_time(c.dest, self.times[k_list[i]]))
        self.times[x] = self.times[k_list[i]]
        self.times.pop(k_list[i])
        k_list[i] = x
        i += 1
        while i < len(k_list)-1:  # update the times of the later floors
            x = str(float(k_list[i]) + self.travel_time(self.times[k_list[i]], self.times[k_list[i + 1]]))
            k_list[i + 1] = x
            self.times[x] = self.times[k_list[i + 1]]
            self.times.pop(k_list[i + 1])
        self.times[str(dest_time)] = c.dest

    def highest_floor(self):
        """
        find the highest floor in times
        :return: highest floor
        """
        max_floor = self.min_floor
        for key in self.times.keys():
            if self.times[key] >= max_floor:
                max_floor = self.times[key]
        return max_floor

    def lowest_floor(self):
        """
        find the lowest floor in times
        :return: lowest floor
        """
        min_floor = self.max_floor
        for key in self.times.keys():
            if self.times[key] <= min_floor:
                min_floor = self.times[key]
        return min_floor

    def get_pos(self, time):
        """
        check the current position of the elevator
        :param time: the time in which we want to check the elevator position
        :return: floor number
        """
        if len(self.times) == 0:  # first call
            return 0
        dict(sorted(self.times.items(), key=lambda item: float(item[0])))
        k_list = list(self.times.keys())
        i = 0
        while i < len(k_list)-1 :
            if float(k_list[i]) <= time <= float(k_list[i+1]):
                break
            i += 1
        if i == len(k_list)-1:  # the elevator finished it's last call
            return self.times[k_list[i]]
        last_time = float(k_list[i])
        last_floor = self.times[k_list[i]]
        for j in range(self.times[k_list[i]], self.times[k_list[i+1]]):
            if self.travel_time(last_floor, j) + last_time > time:
                return j
        return self.times[k_list[i]]

    def get_direction(self, time):
        """
        check the current direction of the elevator
        :param time: the time in which we want to check the elevator direction
        :return: the direction (0 = level, 1 = up, -1 = down)
        """
        if len(self.times) == 0:
            return 0
        dict(sorted(self.times.items(), key=lambda item: item[0]))
        k_list = list(self.times.keys())
        i = 0
        if self.calls[0].time <=time:
            if self.times[k_list[0]] > 0:
                return 1
            else:
                return -1
        while i < len(k_list)-1:
            if float(k_list[i]) <= time <= float(k_list[i+1]):
                if self.times[k_list[i]] < self.times[k_list[i+1]]:
                    return 1
                return -1
            i += 1
        return 0

    def travel_time(self, src, dest):
        """
        calculate travel time between two floors
        :param src: the source floor
        :param dest: the destination floor
        :return: the calculated travel time
        """
        start = self.start_time
        stop = self.stop_time
        open_t = self.open_time
        close_t = self.close_time
        dist = (abs((src - dest))/ float(self.speed))
        #if src == dest:
         #   return close_t + open_t

        return start + stop + open_t + close_t + dist