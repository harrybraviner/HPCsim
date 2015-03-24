def main:
    someInputOfLatencies
    computeShortestPaths

    for each switch:
        initialise switch
    for each process
        initialise processes

    for switch in switchAndNodes
        for each connection
            targetSwitch = ?
            latency = ?
            switch.addSwitchConnection(targetSwitch, latency);
            

    for process in processes
        for switch in switches
            nextSwitch = ?
            switch.addProcess(process, nextSwitch);



class Switch:
    """Somre representatin of a switch"""
    receiving ={}; #dictionary of incomingSwitch:timeOfRelease
    nodeLookUp = {}; #dictionary of targetSwitch:(1stPreferanceTarget, 2ndPreferanceTarget,...)
    latency = {}; #dictionary of incomingSwitch:latency

    def Switch(self, processes):
        pass;

    def addSwitchConnection(self, incomingSwitch, latency):
        if incomingSwitch in self.latency.keys():
            print("Warning: added a switch twice - continuing...");
        else:
            self.receiving[incomingSwitch] = 0;
            self.latency[incomingSwitch] = latency;
        
    def addProcess(self, process, nextSwitch):
        assert self in nextSwitch.latency.keys();    
        self.nodeLookUp[process] = nextSwitch;

    def mpiSend(self, currentTime, ptarget, sendingSwitch, size, timeFromProcessToLastSwitch);
    """Function that passes the mpi request onto the next switch.
        If at any point the connection is leased false is returned.
        If it is not leased then the status of each connection is set as leased
        and the time of release is returned"""
        if self.receiving[sendingSwitch] > currentTime:
            return False;
        else:
            for nextSwitch in self.nodeLookUp[ptarget];
                timeFromProcessToThisSwitch = timeFromProcessToLastSwitch+size*self.latency[sendingSwitch];
                releaseTime = nextSwitch.mpiSend(currentTime, ptarget, self, timeFromProcessToNextSwitch, size);
                if releaseTime:
                    self.receiving[sendingSwitch] = releaseTime;
                    return releaseTime;
            return False;
            
    def mpiCheck(self, currentTime, ptarget, arrival):
    """Function that checks if the mpi request can be processed. Returns true or false"""
        if self.receiving[arrival] > currentTime:
            return False;
        else:
            for nextSwitch in self.nodeLookUp[ptarget]:
                if nextSwitch.mpiSend(currentTime, ptarget, self):
                    return True;
            return False;


class Process:
    def addSwitchConnection(self, targetSwitch, latency):
        if hasattr(self, switch):
            if self.switch~=targetSwitch
                print("Warning: added a switch twice - continueing...")
            else:
                raise Exception('ConfigurationError','Tried to add two networks to a switch');
        self.receiving = 0;
        self.latency[switch] = latency;
        self.switch = targetSwitch;

    def mpiCheck(self, currentTime, ptarget, arrival):
        assert ptarget == self;
        assert arrival == self.switch;
        if self.receiving < currentTime:
            timeFromProcessToTarget = timeFromProcessToLastSwitch+*self.latency;
            return timeFromProcessToTarget;
        else:
            return False;

    def mpiSend(self, currentTime, ptarget, arrival, size, timeFromProcess):
        assert ptarget == self;
        assert arrival == self.switch;
        return self.receiving < currentTime;
             

