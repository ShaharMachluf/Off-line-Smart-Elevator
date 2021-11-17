

class Call:
    def __init__(self, namelist):

        self.time = float(namelist[1])
        self.src = int(namelist[2])
        self.dest = int(namelist[3])
        self.status = int(namelist[4])
        self.elevator = int(namelist[5])