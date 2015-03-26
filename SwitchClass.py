# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:05:18 2015

@author: User
"""
class Switch:
 """Somre representatin of a switch"""
 wct=0

 def __init__(self, processes):
  self.receiving ={}; #dictionary of incomingSwitch:timeOfRelease
  self.nodeLookUp = {}; #dictionary of targetSwitch:(1stPreferanceTarget, 2ndPreferanceTarget,...)
  self.latency = {}; #dictionary of incomingSwitch:latency
  
 def addSwitchConnection(self, incomingSwitch, delay):
  if incomingSwitch in self.latency.keys():
   print("Warning: added a switch twice - continuing...");
  else:
   self.receiving[incomingSwitch] = 0;
   incomingSwitch.receiving[self] = 0;
   self.latency[incomingSwitch] = delay;
   incomingSwitch.latency[self] = delay;
  
 def addProcess(self, process, nextSwitch):
  assert self in nextSwitch.latency.keys(); 
  self.nodeLookUp[process] = nextSwitch;


 def SwitchSend(self, ptarget, SendingTime):
  """Function that passes the mpi request onto the next switch.
   If at any point the connection is leased false is returned.
   If it is not leased then the status of each connection is set as leased
   and the time of release is returned"""
 
  if self.receiving[ptarget] > Switch.wct:
   return False;
  else:
   if SendingTime:
    self.receiving[ptarget] = SendingTime + Switch.wct;
    ptarget.receiving[self] = SendingTime + Switch.wct;
    return True
   return False;
   
 def mpiCheck(self, ptarget, arrival):
  """Function that checks if the mpi request can be processed. Returns true or false"""
  if self.receiving[arrival] > Switch.wct:
   return False;
  else:
   for nextSwitch in self.nodeLookUp[ptarget]:
    if nextSwitch.mpiSend(Switch.wct, ptarget, self):
     return True;
   return False;
   
   
   
   
   
   
   