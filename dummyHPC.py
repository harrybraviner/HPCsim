#! /usr/bin/python2.7

from Process import Process

## dummyHPC class
## This is a temporary measure intended for easy and transparent debugging
## of the Process objects.

class dummyHPC:
    def __init__(self):
        self.procList = []  # List holding all of the processes
        self.wct = 0.0      # Wall-clock time
	
    def addProc(self, N, iL, lambd, tmean):
        self.procList.append(Process(N, iL, self, lambd, tmean))

    def findProcL(self, iL):
        # Function to allow a process to look for the process to the left of it
        # We're looking for a process for which the right-most element (P.iL + P.N)
        # is immediately to the left of the left-most element of the calling function (iL)
        retProc = None
        for P in procList:
            if (P.iL + P.N) == iL - 1:
                retProc = P
        return retProc

    def findProcR(self, iR):
        # Function to allow a process to look for the process to the right of it
        # We're looking for a process for which the left-most element (P.iL)
        # is immediately to the right of the right-most element of the calling function (iR)
        retProc = None
        for P in procList:
            if P.iL == iR + 1:
                retProc = P
        return retProc
