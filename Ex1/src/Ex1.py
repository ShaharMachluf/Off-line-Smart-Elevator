import json
import csv
import numpy as np
import self as self

from Assignments.Ex1.src.call import Call
from Assignments.Ex1.src.building import Building





                                          # build the list and the building by the name of files
def check_bound( calls , b1): #check if it is in bound of the building
    for i in range (len(calls)):
        if int(calls[i].dest)> b1.maxFloor or int(calls[i].src)< b1.minFloor:
            raise  ValueError('this calls dont match for the building')

def start(b1,my_list,my_ans): # alocat the faster elev to the first call
        elev = b1.get_elevator(0)
        my_ans.append(my_list[0])
        my_ans[0][5] = elev.id
        elev.add_call(calls[0])
        elev.set_pos(calls[0])

def algo( call,num,b1,my_ans,calls,my_list): # the algoritem
    direction = 0
    if call.src>call.dest:
        direction=1
    else:
         direction=-1
    temp=-1
    flag=0
    minimum=1000000
    for i in range(len(b1.elevators)): # check if the elvator is in the same floor of the call
        pos=b1.get_elevator(i).get_pos(call.time)
        elev=b1.get_elevator(i)
        if pos == call.src:
            b1.get_elevator(i).add_call(call)
            elev.set_pos(calls[i])
            my_ans.append(my_list[num])
            my_ans[num][5] = elev.id
            return
        else:
            if(elev.get_direction(call.time) == direction) and (minimum>abs(int(pos-call.src))):     #check if there elev same direction and close to the call
                minimum=pos-call.src
                temp=i

    if temp != -1:

        elev = b1.get_elevator(temp)
        my_ans.append(my_list[num])
        my_ans[num][5] = elev.id
        b1.get_elevator(temp).add_call(call)
        elev.set_pos(calls[temp])
        return

    if flag != 1 and temp==-1:
        for i in range(len(b1.elevators)):  #serch the cloest elev and alocat it
            elev = b1.get_elevator(i)
            if elev.get_direction(call.time)==0:
                pos=b1.get_elevator(i).get_pos(call.time)
                if pos-call.src < minimum:
                    minimum=pos-call.src
                    temp=i
    if temp!=-1:

        elev = b1.get_elevator(temp)
        my_ans.append(my_list[num])
        my_ans[num][5] = elev.id
        b1.get_elevator(temp).add_call(call)
        elev.set_pos(calls[temp])
    if flag != 1 and temp ==-1:
        elev = b1.get_elevator(0)
        my_ans.append(my_list[num])
        my_ans[num][5] = elev.id
        b1.get_elevator(0).add_call(call)
        elev.set_pos(calls[0])




if __name__=="__main__":
    myinput=input("anter the names of building file , calls file , output file :")
    myinput =myinput.split(' ')
    my_building=myinput[0]
    my_calls=myinput[1]
    # pathb="C:/Users/shaim/PycharmProjects/OOP_2021/Assignments/Ex1/data/Ex1_input/Ex1_Buildings/"
    # my_building=pathb+my_building
    # pathc="C:/Users/shaim/PycharmProjects/OOP_2021/Assignments/Ex1/data/Ex1_input/Ex1_Calls/"
    # my_calls=pathc+my_calls
    output= myinput[2]
    b1 = Building(my_building)
    my_ans = []
    ans = output
    my_list =[]
    try:
        with open(my_calls, "r") as f:
            reader = csv.reader(f)
            my_list = list(reader)
        calls = []
        for rows in range(len(my_list)):
               calls.append(Call(my_list[rows]))
    #    sorted_elevetor= b1.elevators.sort()
        b1.elevators.sort(key=lambda x: x.speed ,reverse=True)
        check_bound(calls,b1)
        start(b1,my_list,my_ans)

        for i in range(1, len(my_list)):
            algo(calls[i], i,b1,my_ans,calls,my_list)

            np.savetxt("out.csv", my_ans, delimiter=",", fmt='% s')
            #    with open(ans, "w") as csv_file:
            #    writer = csv.writer(csv_file, delimiter=',')
            #      writer.writerows(my_ans)
           # for line in my_ans:
            #    writer.writerow(my_ans[line])

    except FileNotFoundError:
        print("file not found")

