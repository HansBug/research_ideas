#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8531.81852a8bc modeling language!
# line 6 "../../garage_door_direct.ump"
from enum import Enum, auto

class GarageDoor():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #GarageDoor State Machines
    class Status(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Open = auto()
        Closing = auto()
        Closed = auto()
        Opening = auto()
        HalfOpen = auto()

    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._status = None
        self.setStatus(GarageDoor.Status.Open)

    #------------------------
    # INTERFACE
    #------------------------
    def getStatusFullName(self):
        answer = self._status.__str__()
        return answer

    def getStatus(self):
        return self._status

    def buttonOrObstacle(self):
        wasEventProcessed = False
        aStatus = self._status
        if aStatus == GarageDoor.Status.Open :
            self.setStatus(GarageDoor.Status.Closing)
            wasEventProcessed = True
        elif aStatus == GarageDoor.Status.Closing :
            self.setStatus(GarageDoor.Status.Opening)
            wasEventProcessed = True
        elif aStatus == GarageDoor.Status.Closed :
            self.setStatus(GarageDoor.Status.Opening)
            wasEventProcessed = True
        elif aStatus == GarageDoor.Status.Opening :
            self.setStatus(GarageDoor.Status.HalfOpen)
            wasEventProcessed = True
        elif aStatus == GarageDoor.Status.HalfOpen :
            self.setStatus(GarageDoor.Status.Opening)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def reachBottom(self):
        wasEventProcessed = False
        aStatus = self._status
        if aStatus == GarageDoor.Status.Closing :
            self.setStatus(GarageDoor.Status.Closed)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def reachTop(self):
        wasEventProcessed = False
        aStatus = self._status
        if aStatus == GarageDoor.Status.Opening :
            self.setStatus(GarageDoor.Status.Open)
            wasEventProcessed = True
        else :
            # Other states do respond to this event
            pass
        return wasEventProcessed

    def setStatus(self, aStatus):
        self._status = aStatus

    def delete(self):
        pass

