import math
import random

# FIXME FIXME FIXME - you need to add a load of self.'s before lots of member variables in here

class Process:
    narith = 4 # number of FLOPs needed to compute one value
    rstencil = 1 # the radius of the numerical stencil needed to compute one value
                 # It makes NO sense to change this at the moment since we don't have
                 # support for different buffer sizes.
    problemWidth = 50   # Total width of the problem. Used to work out which
                        # elements do NOT need to have values communicated to them
                        # by virtue of 
    def __init__(self, N, iL, parent, lambd, tmean):
        self.N = N      # Number of elements we're responsible for computing
        self.iL = iL    # index of the left-most array element we're responsible for calculating
        self.parent = parent    # Points to the parents node
        self.lambd = lambd  # Parameter to the exponential distribution I'm using for FLOP times
        self.tmean = tmean  # Mean time to do a FLOP
        self.j = 0       # Initial condition - time is zero
        self.tnext = 0   # Initial condition - the next time this process finishes a computation
                         # zero since it has to be in the future for it to be noticed
        self.tarrive = []   # Schedule of times at which packets will arrive
        self.LNC = iL; self.RNC = iL + N - 1; # We have not computed anything yet
        self.procL = None; self.procR = None; # Processes to the left and right in the computational domain
                                    # These are set up in the setup() function
        self.wL = 0; self.wR = 0;   # Number of 'buffer' elements to the left and right that
                                    # we know FOR LEVEL j+1.
        def action():   # Function that holds the changes of state to be performed
            None        # between the current state and tnext

        self.action = action
                       

    def setup(self):
        if (self.iL != 0):
            # If we are NOT touching the left boundary
            self.procL = self.parent.findProcL(self.iL)
            # FIXME - write a function findProcL in the switch class
            # that searches for the process with iL + N equal to the the calling value
        else:
            self.procL = None

        if (self.iL + self.N != self.problemWidth - 1):
            # If we are NOT touching the right boundary
            self.procR = self.parent.findProcR(self.iL + self.N)
            # FIXME - write a function findProcR in the switch class
            # that searches for the process with iL equal to the the calling value
        self.update()

    def tComp(self):
        # Return a random variable for how long a FLOP took
        return (self.tmean - 1.0/self.lambd + random.expovariate(self.lambd))

    def tComps(self, n):
        # Return a random variable for how long n FLOPs took
        retVar = n*self.tmean
        retVar -= n*(1.0/self.lambd)
        retVar += sum([random.expovariate(self.lambd) for x in range(n)])
        return retVar

    
    def nextUpdate(self, t0):
        # This function is used to enable to HPC simulation to work out what the
        # next process to interact with the rest of the network will be
        return tnext

    def update(self):
        ## This is the section that should have some scope for being modified
        ## to implement different strategies
        ## Current idea:
        ##  Calculate the outer-most points first so they can be sent to our neighbours

        # First - perform any update that will have occurred since this function was
        # last called
        self.action()
        
        ## Have we computed the points at the left and right ends of the domain
        ## so that we can send them to our neighbours?
        if (self.LNC == self.iL): 
            ## Compute the left-most point so we can send it to our left-ward neighbour
            def action():
                self.LNC +=1
            self.action = action
            self.tnext += self.tComp()
        elif (self.RNC == self.iL + self.N - 1):
            ## Compute the right-most point so we can send it to our right-ward neighbour
            def action():
                self.RNC -=1
            self.action = action
            self.tnext += self.tComp()
        else:
            ## If we get here we can just do the rest of our computation at this
            ## level and not worry about having to send any of it over the network
            def action():
                self.LNC = None
                self.RNC = None
                self.j += 1     # We will have computed everything and may move to the next level
            self.action = action
            if self.RNC is not None:
                if self.LNC is not None:
                    self.tnext += self.tComps(self.RNC - self.LNC + 1)
        # FIXME - put in communication calls, test against dummy HPC
