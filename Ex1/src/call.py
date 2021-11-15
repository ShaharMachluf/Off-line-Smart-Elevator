import csv

    class call:
       
            def __init__(self, namelist):
                try:
                    with open(namelist, "r") as f:
                        reader =csv.reader(f)
                        self.time = reader[1]
                        self.src = reader[2]
                        self.dest = reader[3]
                        self.status = reader[4]
                        self.elevator = reader[5]
                except FileNotFoundError:
                    print("file not found")
