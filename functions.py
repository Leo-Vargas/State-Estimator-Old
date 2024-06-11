import numpy as np
import math
from classes import Measurement, StateData


# ----------------------- Data Processing Related Functions -----------------------------
def createGridTopology(Ybus: np.array):
    
    
    gridTopology = {}
    keys = range(1, Ybus.shape[0] + 1)
    for i in keys:
        gridTopology[i] = set()

    print(gridTopology)

    for y in range(Ybus.shape[0]):
        for x in range(y + 1, Ybus.shape[1]):
            if Ybus[x,y] != 0:
                gridTopology[x+1].add(y+1)
                gridTopology[y+1].add(x+1)

    print(gridTopology)
    return gridTopology                
         


def hSetup(gridTopology: dict):
    hValues = np.ones(((len(gridTopology)*2)-1), dtype=float)
    topologyList = list(gridTopology.keys())
    hDataDict = {}
    
    for i in range((len(gridTopology)*2)-1):
        if i < len(gridTopology)-1:
            hValues[i]=0.0
            hDataDict.update({'a'+str(topologyList[i+1]): StateData(0, i, topologyList[i+1])})
        else:
            hDataDict.update({'v'+str(topologyList[i-(len(gridTopology)-1)]): StateData(1, i, topologyList[i-(len(gridTopology)-1)])})

    hDataDictUpdate(hValues, hDataDict)

    return [hValues, hDataDict]

def hDataDictUpdate(hvalues: np.ndarray, hDataDict: dict):
   
    for i, (key, hData) in enumerate(hDataDict.items()):
        hData.addValue(hvalues[i])
        


# --------------------- Print Functins ---------------------------------
def PrintStateData(hDataDict: dict):
    hDataList = list(hDataDict.values())
    
    print(f'bar 1: Voltage: {hDataList[math.floor(len(hDataList)/2)].value[-1]} Angle: 0')
    for i in range(math.floor(len(hDataList)/2)):
        print(f'bar {hDataList[i].bus}: Voltage: {hDataList[i+math.ceil(len(hDataList)/2)].value[-1]} Angle: {hDataList[i].value[-1]*180/math.pi}')
    
    print('\n')
        
def PrintEstimatedValuesData(measurementDict, estimatedValues, residuals):
    
    for i, (key, measurement) in enumerate(measurementDict.items()):
        print(f'Measurement {key}: Value: {measurement.value} Estimated Value: {estimatedValues[i]} Residual: {residuals[i]}')
        
    print('\n')
