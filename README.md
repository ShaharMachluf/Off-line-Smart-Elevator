
# OOP_ariel
Off-line smart elevator algorithm

## Bibiliografy:
- https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup
- https://github.com/joeblau/sample-elevator-control-system
- https://studylib.net/doc/7878746/on-line-algorithms-versus-off-line-algorithms-for-the-ele

The purpose of this algorithm is to allocate elevators in the building to calls for elevators that are given as input before hand.
the algorithm's efficiency is measured by the everage wait time (from the time of the call to the arrival to the destination. 

## Algorithm:
input: call time, source floor, destination floor
- allocate the fastest elevator to the first call.
- check if there is an elevator in the source floor and allocate it.
- Else, check if there is an elevator going to the same direction and going through the source floor with minimal stops.
- Else, check if there is an elevator going to the nearest dest to the source floor.
- By default: allocate the fastest elevator


<img width="751" alt="2021-11-18 (2)" src="https://user-images.githubusercontent.com/85555432/142399177-67ba6531-6a20-42be-83d6-00d9408294fb.png">
