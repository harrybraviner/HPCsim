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
                        # by virtue of being at a boundary
    def __init__(self, N, iL, parent, lambd, tmean):
        self.N = N      # Number of elements we're responsible for computing
        self.iL = iL    # index of the left-most array element we're responsible for calculating
        self.parent = parent    # Points to the parents node
        self.lambd = lambd  # Parameter to the exponential distribution I'm using for FLOP times
        self.tmean = tmean  # Mean time to do a FLOP
        self.j = 0          # Initial condition - timestep is zero
        self.tnext = 0      # Initial condition - the next time this process finishes a computation
                            # zero since it has to be in the future for it to be noticed
        self.tsend = None   # Time at which we will next check if we are able to send across the network
        self.LNC = iL; self.RNC = iL + N - 1; # We have not computed anything yet
        self.procL = None; self.procR = None; # Processes to the left and right in the computational domain
                                    # These are set up in the setup() function
        self.WL = [None]; self.WR = [None]; # Times at which we will receive the 'buffer' elements to the
                                            # left and right that FOR LEVEL j+1.
        self.XL = [False]; self.XR = [False];   # Have we sent the data that needs to go to the left
                                                # and right processes yet?
        def action():   # Function that holds the changes of state to be performed
            None        # between the current state and tnext

        self.action = action
                       

    def setup(self):
        if (self.iL != 0):
            # If we are NOT touching the left boundary
            self.procL = self.parent.findProcL(self.iL)
        else:
            self.procL = None
            self.WL = []    # FIXME - dirty hack, this will let us continue computing
                            #         even if this process was simply missing, rather 
                            #         than us being at the left-hand boundary!

        if (self.iL + self.N - 1 != self.problemWidth - 1):
            # If we are NOT touching the right boundary
            self.procR = self.parent.findProcR(self.iL + self.N - 1)
        else:
            self.procR = None
            self.WR = []    # FIXME - dirty hack, this will let us continue computing
                            #         even if this process was simply missing, rather 
                            #         than us being at the left-hand boundary!

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

    def mpiRecv(self, transTime, sendProc):
        if self.j != sendProc.j:
            return False
        ## We have just had data transferred to us from another processor
        if(sendProc == self.procL):
            self.WL[0] = self.parent.wct + transTime
            if self.tnext is None:
                def action():
                    None
                self.action = action
                self.tnext = self.WL[0]
        if(sendProc == self.procR):
            self.WR[0] = self.parent.wct + transTime
            if self.tnext is None:
                def action():
                    None
                self.action = action
                self.tnext = self.WR[0]
        return True # Success

    def send(self):
        ## This gets called every time by the update function
        ## We check if we have any unsent data that needs to be sent
        ## We see if we can lease a network connection to do so
        ## If we can, we send that data

        tMinWait = None

        # Do we have data to send to the left processor?
        if (self.LNC > self.iL and self.procL is not None) and any([not x for x in self.XL]):
            # Are we able to make the connection now?
            tWait = self.parent.mpiSend(self, self.procL, 1)
            if (tWait == 0):
                self.XL = [True]     # All the data is on its way
            else:
                # Is this communication the soonest one that we should attempt?
                if (tMinWait is None or tWait < tMinWait):
                    tMinWait = tWait

        # Do we have data to send to the right processor?
        if (self.RNC < self.iL + self.N - 1 and self.procR is not None and any([not x for x in self.XR])):
            # Are we able to make the connection now?
            tWait = self.parent.mpiSend(self, self.procR, 1)
            if (tWait == 0):
                self.XR = [True]     # All the data is on its way
            else:
                # Is this communication the soonest one that we should attempt?
                if (tMinWait is None or tWait < tMinWait):
                    tMinWait = tWait

        # If we are waiting for a communication channel to become available,
        # note this down in self.tsend
        self.tsend = tMinWait
                


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
                self.send() # Handles invoking mpiSend
            self.action = action
            self.tnext += self.tComp()
        elif (self.RNC == self.iL + self.N - 1):
            ## Compute the right-most point so we can send it to our right-ward neighbour
            def action():
                self.RNC -=1
                self.send() # Handles invoking mpiSend
            self.action = action
            self.tnext += self.tComp()
        elif (self.LNC is not None and self.RNC is not None):
            ## The boundary points that we want to transmit have all been computed,
            ## but we still have the interior of this level to compute
            ## If we get here we can just do the rest of our computation at this
            ## level and not worry about having to send any of it over the network
            def action():
                self.LNC = None
                self.RNC = None
                #self.j += 1     # We will have computed everything but may not necessarrily
                                 # move to the next level since data may not have arrived at us
            self.action = action
            self.tnext += self.tComps(self.RNC - self.LNC + 1)
        elif (self.LNC is None and self.RNC is None):
            ## We have completed the entire computation at level j
            ## Has all of the data we need to compute level j+1 arrived?
            if all([(x is not None and x <= self.tnext)for x in self.WL + self.WR]):
                self.j += 1
                self.WL = [None for x in self.WL]
                self.WR = [None for x in self.WR]   # This is now the buffer for the NEXT level
                self.XL = [False]; self.XR = [False];   # We haven't sent anything for this level yet
                self.LNC = self.iL; self.RNC = self.iL + self.N - 1;
                def action():
                    None
                self.action = action
                self.update()   # This is to get the first computation from the j+1 step to run
            else:
                ## We cannot compute the next level yet
                ## Wait for data
                def action():
                    None
                self.action = action
                # FIXME - something is seriously wrong here. Sometimes (and just sometimes)
                #         this tries to find min([]), and I don't understand why!
                self.tnext = min([t for t in self.WL + self.WR if (t is not None and t > self.tnext)])

        # FIXME - put in communication calls, test against dummy HPC
