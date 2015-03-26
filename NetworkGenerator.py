# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:24:10 2015

@author: User
"""

from math import floor
from ProcessClass import Process
from SwitchClass import Switch

def chainGeneration ( numSwitch, numProc, N, lambd, tmean ):
 SwitchList = []
 SwitchList.append(Switch(0))
 
 for i in range(numSwitch-1):
  SwitchList.append(Switch(0))
  SwitchList[i].addSwitchConnection(SwitchList[i+1],1)

 ProcessList = []
 
 for i in range(numSwitch):
  for j in range(numProc):
   ProcessList.append(Process(N/(numSwitch*numProc),i*numProc+j,SwitchList[i],lambd,tmean))
 return SwitchList, ProcessList



def binaryTreeGeneration ( levels, numProc, N, lambd, tmean ):
 SwitchList = []
 SwitchList.append(Switch(0))

 for i in range(2**(levels+1)-2):
  SwitchList.append(Switch(0))
  SwitchList[i+1].addSwitchConnection(SwitchList[int(floor(i/2))],1)

 ProcessList = []
 
 for i in range(2**levels):
  for j in range(numProc):
   ProcessList.append(Process(N/(2**levels*numProc),N/(2**levels*numProc)*(i*numProc+j),SwitchList[2**levels-1+i],lambd,tmean))
 
 return SwitchList, ProcessList