# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:40:08 2015

@author: User
"""
from ProcessClass import Process
from SwitchClass import Switch
from SendingFunctions import SendData 
import NetworkGenerator


def main():
 SwitchList,ProcessList=NetworkGenerator.binaryTreeGeneration ( 3, 2, 10000, 1000, 1 )
 print ProcessList[0].parent.wct
 print ProcessList[0].mpiSend(SwitchList,ProcessList[5],1)
 Switch.wct=10
 print ProcessList[0].parent.wct
 print ProcessList[0].mpiSend(SwitchList,ProcessList[5],1)
 
 
 
 
