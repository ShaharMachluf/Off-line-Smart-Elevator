import json
import csv

import self as self

from Assignments.Ex1.src.call import Call
from Assignments.Ex1.src.building import Building
from Assignments.Ex1.src.simulator import Simulator, direction


class Ex1:
    def __init__(self ,my_building , my_calls , output ):
        self.b1=Building(my_building)
        self.my_ans=[]

        try:
            with open(my_calls, "r") as f:
                reader = csv.reader(f)
                self.my_list=list(reader)
            self.calls = []
            for rows in range(len(self.my_list)):
                self.calls.append(Call(self.my_list[rows]))
            self.b1.elevators.sort(lambda x: x.speed)
            self.check_bound()
            self.start()

        except FileNotFoundError:
            print("file not found")


    def check_bound(self): #check if it is in bound
        for i in range (len(self.calls)):
             if self.calls[i].dest>self.b1.maxFloor or self.calls[i].src<self.b1.minFloor:
                raise  Exception("this calls dont match for the building")

    def start(self):
        elev = self.b1.get_elevator(0)
        sim = Simulator(elev)
        self.my_ans.append(self.my_list[0])
        self.my_ans[0][6] = elev.id
        elev.add_call(self.calls[0])
        sim.set_pos(self.calls[0])



    def algo(self, call):
        direction = 0
        if call.src>call.dest:
            direction=1
        else:
            direction=-1
        temp=0
        minimum=1000000
        for i in range(len(self.b1.elevators)):
            sim=Simulator(self.b1.get_elevator(i))
            pos=self.b1.get_elevator(i).get_pos()
            if pos == call.src:  #how we know the pos
                self.b1.get_elevator(i).add_call(call)
                sim.set_pos(self.calls[i])
                break
            else:
                if(sim.get_direction(call.time) and direction) and (minimum>pos-call.src):
                    minimum=pos-call.src
                    temp=i
            if temp != 0:
                self.b1.get_elevator(temp).add_call(call)
                sim.set_pos(self.calls[temp])

        temp=0
        for i in range(len(self.b1.elevators)):
            sim=Simulator(self.b1.get_elevator(i))
            pos=self.b1.get_elevator(i).get_pos()
            if pos-call.src < minimum:
                minimum=pos-call.src
                temp=i

        self.b1.get_elevator(temp).add_call(call)
        sim.set_pos(self.calls[temp])

