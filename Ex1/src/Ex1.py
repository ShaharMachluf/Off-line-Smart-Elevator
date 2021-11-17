import json
import csv

import self as self

from Assignments.Ex1.src.call import Call
from Assignments.Ex1.src.building import Building
from Assignments.Ex1.src.simulator import Simulator, direction


class Ex1:
    def __init__(self ,my_building , my_calls , output):  # build the list and the building by the name of files
        self.b1=Building(my_building)
        self.my_ans=[]
        self.ans=output
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

    def main(self):
        i=1
        for i in range(len(self.my_list)):
            self.algo(self.my_list[i],i)

        with open( self.ans, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in self.my_ans:
                writer.writerow(self.my_ans[line])

    def check_bound(self): #check if it is in bound of the building
        for i in range (len(self.calls)):
             if self.calls[i].dest>self.b1.maxFloor or self.calls[i].src<self.b1.minFloor:
                raise  Exception("this calls dont match for the building")

    def start(self): # alocat the faster elev to the first call
        elev = self.b1.get_elevator(0)
        sim = Simulator(elev)
        self.my_ans.append(self.my_list[0])
        self.my_ans[0][6] = elev.id
        elev.add_call(self.calls[0])
        sim.set_pos(self.calls[0])



    def algo(self, call,num): # the algoritem
        direction = 0
        if call.src>call.dest:
            direction=1
        else:
            direction=-1
        temp=0
        flag=0
        minimum=1000000
        for i in range(len(self.b1.elevators)): # check if the elvator is in the same floor of the call
            sim=Simulator(self.b1.get_elevator(i))
            pos=self.b1.get_elevator(i).get_pos()
            if pos == call.src:
                self.b1.get_elevator(i).add_call(call)
                sim.set_pos(self.calls[i])
                elev= self.b1.get_elevator(i)
                self.my_ans.append(self.my_list[num])
                self.my_ans[num][6] = elev.id
                flag=1
                break
            else:
                if(sim.get_direction(call.time) and direction) and (minimum>pos-call.src):     #check if there elev same direction and close to the call
                    minimum=pos-call.src
                    temp=i

        if temp != 0:
            elev = self.b1.get_elevator(temp)
            self.my_ans.append(self.my_list[num])
            self.my_ans[num][6] = elev.id
            self.b1.get_elevator(temp).add_call(call)
            sim.set_pos(self.calls[temp])
            flag=1


        if flag!=1 and temp==0:
            for i in range(len(self.b1.elevators)):  #serch the cloest elev and alocat it
                sim=Simulator(self.b1.get_elevator(i))
                pos=self.b1.get_elevator(i).get_pos()
                if pos-call.src < minimum:
                    minimum=pos-call.src
                    temp=i
        if temp!=0:
            elev = self.b1.get_elevator(temp)
            self.my_ans.append(self.my_list[num])
            self.my_ans[num][6] = elev.id
            self.b1.get_elevator(temp).add_call(call)
             sim.set_pos(self.calls[temp])

