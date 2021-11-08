import csv

    class Calls:
        _Time=0.0
        _Src=0
        _dest=0
        _status=0
        _elevator=-1

        def __init__(self,namelist):
            self._Time=namelist[1]
            self._Src=namelist[2]
            self._dest=namelist[3]
            self._status=namelist[4]
            self._elevator=namelist[5]