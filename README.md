HPCsim
======

Written as part of the 107th ESGI as a simulator for the network congestion
of a high performance computer.

## Model

Each process is modelled as a `Process` object.
These will eventually communicate via their `parent` member variable, an object representing the HPC network.
Evenutally this will be a graph of `Switch` objects.
Currently it is being mimicked by the `dummyHPC` object.

Time is in units of milliseconds.

## The `Process` object

The process object retatins the state of how much of the next timestep we've calculated.
We store which elements of the field have been computed as follows:
* `j` - the last timestep which was fully computed
* `f[iL, iL + N]` - elements this process is responsible for computing.
* `f[iL - rstencil, iL + N + rstencil]` - buffer of elements that this process is happy to accept.
* `LNC` and `RNC` - the bounds of the array that has *not* been computed.
  Only these are explicitly represented, rather than `f`.

At this stage I'm assuming that the *buffer* at the left and right ends of our computational domain
is the size of the numerical stencil - i.e. we only have sufficient information to compute all of the
elements we're responsible for at the next timestep.

In this version we only compute the next level of the pyramid, and then wait until we have the
end-points from the neighbouring processes before proceeding.

### Overview of how `Process` updates

Each process object holds a time `tnext` at which it next finishes a computation and needs to
do something 'interesting'.
'Interesting' could include interacting with other parts of the network.

When `update` is called, the `Process` object does the following:
* Calls the `action` function, which does the next 'interesting' thing that we decided was going
  to happen at `tnext`.
* Update the `action` function.
* Update `tnext`.

Exactly what the action function is updated to depends on the state of the `Process` and the
computing strategies we wish to test.
This is a very basic strategy at the moment:
* Compute the boundary points, send them to neighbours.
* Compute the rest of the domain.

## Random ideas

* Visualisation functions. Would be nice te be able to 'play' the simulation in a step-forward fashion with breakpoints etc.
* Visualisation of schedule of upcoming events.
  Logarithmic timescale.
  Colour coding for comms versus computing versus idle etc.
