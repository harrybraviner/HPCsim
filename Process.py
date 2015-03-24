import math
import random

class Process:
    narith = 4 # number of FLOPs needed to compute one value
    rstencil = 1 # the radius of the numerical stencil needed to compute one value
    problemWidth = 50   # Total width of the problem. Used to work out which
                        # elements do NOT need to have values communicated to them
                        # by virtue of 
    def __init__(self, N, WL, WR, iL, parent, lambd, tmean):
        self.N = N      # Number of elements we're responsible for computing
        self.WL = WL    # Size of the buffer to the left
        self.WR = WR    # Size of the buffer to the right
        self.iL = iL    # index of the left-most array element we're responsible for calculating
        self.parent = parent    # Points to the parents node
        self.lambd = lambd  # Parameter to the exponential distribution I'm using for FLOP times
        self.tmean = tmean  # Mean time to do a FLOP
        j = 0       # Initial condition - time is zero
        tnext = 0   # Initial condition - the next time this process wants to do anything
                    # zero since it has to be in the future for it to be noticed
                    # FIXME - set this to when we compute a boundary point
        LNC = iL; RNC = iL + N; # We have not computed anything yet
        procL = None; procR = None; # Processes to the left and right in the computational domain
                                    # These are set up in the setup() function

    def setup(self):
        if (iL != 0):
            # If we do not have the left boundary condition
            procL = parent.findProcL(iL)
            # FIXME - write a function findProcL in the switch class
            # that searches for the process with iL + N equal to the the calling value
        else:
            procL = None

        if (iL + N != problemWidth - 1):
            # If we do NOT have the right boundary condition
            procR = parent.findProcR(iL + N)
            # FIXME - write a function findProcR in the switch class
            # that searches for the process with iL equal to the the calling value

    def tComp(self):
        # Return a random variable for how long a FLOP took
        return (tmean - 1.0/lambd + random.expovariate(lambd))

    
    def nextUpdate(self, t0):
        # This function is used to enable to HPC simulation to work out what the
        # next process to interact with the rest of the network will be
        return tnext

    def compute(self):
        # First (if necessary) compute the points that will need to be passed to the
        # processor 'to the left'
        if (LNC <= iL + procLWR)

    def update(self):
        ## This is the section that should have some scope for being modified
        ## to implement different strategies
        ## Current idea:
        ##  Calculate the outer-most points first so they can be sent to our neighbours
        
        ## Is the buffer of the processor to the left or right non-full?
        if (LNC <= ((iL - 1) + procLWR) or RNC >= ((iL + N + 1) - procRWL)): 
            ## Which buffer should I do a computation for?
        else:
            ## If we get here we can just do the rest of our computation at this
            ## level and not worry about having to send any of it over the network
