HPCsim
======

Written as part of the 107th ESGI as a simulator for the network congestion
of a high performance computer.

## Model

Each process is modelled as a `Process` object.

We work in units of milliseconds.

## The `Process` object

The process object retatins the state of how much of the next timestep we've calculated.
We store which elements of the field have been computed as follows:
* `j` - the last timestep which was fully computed
* `f[iL, iL + N]` - elements this process is responsible for computing.
* `f[iL - WL, iL + N + WR]` - buffer of elements that this process is happy to accept.
* `LNC` and `RNC` - the bounds of the array that has *not* been computed.

### Overview of how `Process` updates

Each process object holds a time `tnext` at which it next needs to do anything 'interesting'.
'Interesting' could be interacting with other parts of the network, or getting to the end of its
computational pyramid.

I need to compute this value each time I update the state of a `Process` instance, otherwise
I risk never updating that instance again!
