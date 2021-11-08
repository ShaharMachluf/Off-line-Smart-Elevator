from multiprocessing.resource_sharer import stop


class Elevator:
    _id=0
    _speed=0.0
    _minFloor=0
    _maxFloor=0
    _closeTime=0.0
    _openTime=0.0
    _startTime=0.0
    _stopTime=0.0
    _calls=[]
    def __init__(self,id,speed,minfloor,maxfloor,closetime,opentime,startime,stoptime):
        self._id=id
        self._speed=speed
        self._minFloor=minfloor
        self._maxFloor=maxfloor
        self._closeTime=closetime
        self._openTime=opentime
        self._startTime=startime
        self._stopTime=stoptime

    def getid(self):
        return self._id

    def getstopTime(self):
        return self._stopTime

    def getspeed(self):
        return self._speed

    def getminfloor(self):
        return self._minFloor

    def getmaxfloor(self):
        return self._maxFloor

    def get_closetime(self):
        return self._closeTime

    def get_openTime(self):
        return self._openTime

    def get_startTime(self):
        return self._startTime

    def addcall(self, name):
        self._calls.append(name)