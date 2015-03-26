#! /usr/bin/python2.7

from Process import Process

## dummyHPC class
## This is a temporary measure intended for easy and transparent debugging
## of the Process objects.

class dummyHPC:

    latency = 20.0  # Latency. Crap model. Doesn't care about topology or any sort of stochasticity.

    def __init__(self):
        self.procList = []  # List holding all of the processes
        self.wct = 0.0      # Wall-clock time
        self.wctList = []   # Holds a list of wall clock times from each update
        self.jList = []     # Holds lists of j(t) for each process, appended to at each update
        self.WLList = []    # Has the process received all the left-end data?
        self.WRList = []    # Has the process received all the right-end data?
        self.XLList = []    # Does the process have any left-end data to send?
        self.XRList = []    # Does the process have any right-end data to send?
	
    def getWCT(self):
        return self.wct

    def addProc(self, N, iL, lambd, tmean):
        self.procList.append(Process(N, iL, self, lambd, tmean))

    def setupProcs(self):
        # This has to be called after the processors are added so that they can actually
        # find their left and right neighbours
        for P in self.procList:
            P.setup()

    def findProcL(self, iL):
        # Function to allow a process to look for the process to the left of it
        # We're looking for a process for which the right-most element (P.iL + P.N)
        # is immediately to the left of the left-most element of the calling function (iL)
        retProc = None
        for P in self.procList:
            if (P.iL + P.N - 1) == iL - 1:
                retProc = P
        return retProc

    def findProcR(self, iR):
        # Function to allow a process to look for the process to the right of it
        # We're looking for a process for which the left-most element (P.iL)
        # is immediately to the right of the right-most element of the calling function (iR)
        retProc = None
        for P in self.procList:
            if P.iL == iR + 1:
                retProc = P
        return retProc

    def nextTime(self):
        # Search for the process with the smallest tnext that is greater or equal now
        return reduce(lambda a, b : a if a[1] < b[1] else b,
                      [(P, P.tnext) for P in self.procList if (P.tnext >= self.wct and P.tnext is not None)])

    def update(self):
        # Get the process with the next smallest waiting time
        P, t = self.nextTime()
        # Update the process
        P.update()
        # Everything up to t has now happened, so update the wall-clock time
        self.wct = t
        # Update the data we're storing
        self.wctList.append(self.wct)
        self.jList.append([x.j for x in self.procList])
        self.WLList.append([all([(x is not None and x <= self.wct) for x in P.WL]) for P in self.procList])
        self.WRList.append([all([(x is not None and x <= self.wct) for x in P.WR]) for P in self.procList])
        self.XLList.append([any([(x is True) for x in P.XL]) for P in self.procList])
        self.XRList.append([any([(x is True) for x in P.XR]) for P in self.procList])

    def mpiSend(self, sendProc, recvProc, size):
        # N.B. this is very definitely NOT a decent model for the communication
        # at this stage.
        success = recvProc.mpiRecv(self.latency, sendProc)
        if success:
            return 0 # dummyHPC currently lives in a magical, magical world where there is infinite bandwidth
        else:
            # We're needing to wait for the other process to move to the next level
            # tell me how long this will take
            return recvProc.tnext

    def printToFile(self, outfileName):
        outfile = open(outfileName, "w")
        # Print a header
        outfile.write("#t\t")
        for x in range(len(self.procList)):

            outfile.write("\tXWLP" + str(x));
            outfile.write("\tjP" + str(x));
            outfile.write("\tWXRP" + str(x));
        outfile.write("\n")

        # Write lines for each wall-clock time
        def TF(x):
            if x:
                return "T"
            else:
                return "F"
        for x in range(len(self.wctList)):
            outfile.write(str(self.wctList[x]))
            for y in range(len(self.procList)):
                outfile.write("\t" + TF(self.XLList[x][y]))
                outfile.write(TF(self.WLList[x][y]))
                outfile.write("\t" + str(self.jList[x][y]))
                outfile.write("\t" + TF(self.WRList[x][y]))
                outfile.write(TF(self.XRList[x][y]))
            outfile.write("\n")

        outfile.close()

## Unit testing - everything below here is not part of the object itself

def main():
    print("Creating an HPC...")
    print("HPC = dummyHPC()")
    HPC = dummyHPC()

    print("\nAdding some processes...")
    print("HPC.addProc(10, 0, 1e+3, 1.0)")
    HPC.addProc(10, 0, 1e+3, 1.0)
    print("HPC.addProc(20, 10, 1e+3, 1.0)")
    HPC.addProc(20, 10, 1e+3, 1.0)
    print("HPC.addProc(10, 30, 1e+3, 1.0)")
    HPC.addProc(10, 30, 1e+3, 1.0)
    print("HPC.addProc(10, 40, 1e+3, 1.0)")
    HPC.addProc(10, 40, 1e+3, 1.0)

    print("\nTelling the processes to set themselves up...")
    print("HPC.setupProcs()")
    HPC.setupProcs()

    #print("\nDo 19 updates that I shalln't bother printing...")
    for i in range(400):
        try:
            HPC.update()
        except Exception as e:
            print e
            break

    HPC.printToFile("trace.dat")
    
    print("Creating an second HPC...")
    print("HPC2 = dummyHPC()")
    HPC2 = dummyHPC()

    print("\nAdding some processes...")
    print("HPC2.addProc(10, 0, 1e+3, 1.0)")
    HPC2.addProc(10, 0, 1e+3, 1.0)
    print("HPC2.addProc(15, 10, 1e+3, 1.0)")
    HPC2.addProc(15, 10, 1e+3, 1.0)
    print("HPC2.addProc(15, 25, 1e+3, 1.0)")
    HPC2.addProc(15, 25, 1e+3, 1.0)
    print("HPC2.addProc(10, 40, 1e+3, 1.0)")
    HPC2.addProc(10, 40, 1e+3, 1.0)

    print("\nTelling the processes to set themselves up...")
    print("HPC2.setupProcs()")
    HPC2.setupProcs()

    #print("\nDo 19 updates that I shalln't bother printing...")
    for i in range(400):
        try:
            HPC2.update()
        except Exception as e:
            print e
            break

    HPC2.printToFile("trace2.dat")
    
    print("Creating an third HPC...")
    print("HPC3 = dummyHPC()")
    HPC3 = dummyHPC()

    print("\nAdding some processes...")
    print("HPC3.addProc(5, 0, 1e+3, 1.0)")
    HPC3.addProc(5, 0, 1e+3, 1.0)
    print("HPC3.addProc(5, 5, 1e+3, 1.0)")
    HPC3.addProc(5, 5, 1e+3, 1.0)
    print("HPC3.addProc(5, 10, 1e+3, 1.0)")
    HPC3.addProc(5, 10, 1e+3, 1.0)
    print("HPC3.addProc(5, 15, 1e+3, 1.0)")
    HPC3.addProc(5, 15, 1e+3, 1.0)
    print("HPC3.addProc(5, 20, 1e+3, 1.0)")
    HPC3.addProc(5, 20, 1e+3, 1.0)
    print("HPC3.addProc(5, 25, 1e+3, 1.0)")
    HPC3.addProc(5, 25, 1e+3, 1.0)
    print("HPC3.addProc(5, 30, 1e+3, 1.0)")
    HPC3.addProc(5, 30, 1e+3, 1.0)
    print("HPC3.addProc(5, 35, 1e+3, 1.0)")
    HPC3.addProc(5, 35, 1e+3, 1.0)
    print("HPC3.addProc(5, 40, 1e+3, 1.0)")
    HPC3.addProc(5, 40, 1e+3, 1.0)
    print("HPC3.addProc(5, 45, 1e+3, 1.0)")
    HPC3.addProc(5, 45, 1e+3, 1.0)

    print("\nTelling the processes to set themselves up...")
    print("HPC3.setupProcs()")
    HPC3.setupProcs()

    #print("\nDo 19 updates that I shalln't bother printing...")
    for i in range(400):
        try:
            HPC3.update()
        except Exception as e:
            print e
            break

    HPC3.printToFile("trace3.dat")
    

if __name__ == "__main__":
    main()
