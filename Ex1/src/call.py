

class Call:
    def __init__(self, namelist):

        self.time = namelist[1]
        self.src = namelist[2]
        self.dest = namelist[3]
        self.status = namelist[4]
        self.elevator = namelist[5]