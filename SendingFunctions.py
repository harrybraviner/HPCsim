# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:08:07 2015

@author: User
"""



    
def ShortestPath (graph, source, destination):
 """This function finds the shortest path on graph described by adjacency matrix graph
  between source and destination node. The path is returned as a table of waypoints"""
 index = range(len(graph))
 setToAnalyze=[]
 distance=[]
 previous=[]
 for vortex in index:
  if index!=source:
   distance.append(float('inf'))
   previous.append(None)
  setToAnalyze.append(vortex)

 distance[source] = 0
 previous[source] = None
 
 while len(setToAnalyze):
  vortex = setToAnalyze[0]
  minimum = distance[setToAnalyze[0]]
  for i in setToAnalyze:
   if distance[i]<minimum:
    minimum=distance[i]
    vortex=i
  setToAnalyze.remove(vortex)
  
  for neighbour in index:
   if graph[vortex][neighbour]:
    alt = distance[vortex]+graph[vortex][neighbour]
    if alt<distance[neighbour]:
     distance[neighbour] = alt
     previous[neighbour]=vortex
      
 dist = distance[destination]
 if dist==float('inf'):
  return False,False
 
 path=[destination]
 while destination!=source:
  destination = previous[destination]
  path.insert(0,destination)
 print path
 return path, dist

def SendData(SwitchList,SwitchSend,SwitchGet,packetsize,currentTime):
 """This Funtion takes the network configuration as a whole and two switches
 in it then computes the shortest path between them and sets them to recieving.
 Returning false if a connection cannot be made and the time taken to send
 if it can be connected"""
 Nmatrix=[[float('inf') for x in range(len(SwitchList))] for x in range(len(SwitchList))]
 for i in range(len(SwitchList)):
  for j in range(len(SwitchList)):
    try:
     if SwitchList[i].receiving[SwitchList[j]] <= currentTime:
      Nmatrix[i][j] = float(SwitchList[i].latency[SwitchList[j]])
    except KeyError:
     pass
 source = None
 destination = None 
 for i in range(len(SwitchList)):
  if (SwitchSend==SwitchList[i]):
   source=i
  if (SwitchGet==SwitchList[i]):
    destination=i
  
 path, PathLatency = ShortestPath (Nmatrix,source,destination)
 if path==False:
  return False
 SendingTime=PathLatency+packetsize
 
 for i in xrange(len(path)-1):
  if(SwitchList[path[i]].SwitchSend(SwitchList[path[i+1]], currentTime+SendingTime)==False):
   return False

 return SendingTime
 
def LeastTime(SwitchList,SwitchSend,SwitchGet,packetsize,currentTime):
 """this function finds the time to send a packet if the network was otherwise
 unused and returns the time to send in this case"""
 Nmatrix=[[0 for x in range(len(SwitchList))] for x in range(len(SwitchList))]
 for i in range(len(SwitchList)):
  for j in range(len(SwitchList)):
   Nmatrix[i][j] = float(SwitchList[i].latency[SwitchList[j]])
   if (Nmatrix[i][j]==0):
     Nmatrix[i][j]=float('inf')
 source = None
 destination = None 
 for i in range(len(SwitchList)):
  if (SwitchSend==SwitchList[i]):
   source=i
  if (SwitchGet==SwitchList[i]):
   destination=i
   
  path, PathLatency = ShortestPath (Nmatrix,source,destination)
 if path==False:
  return False
 SendingTime=PathLatency+packetsize
 return SendingTime
 
 
 
 
 
 
 
 
 
 
 