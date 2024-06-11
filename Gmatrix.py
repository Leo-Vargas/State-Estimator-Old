import numpy as np
import math
from classes import Measurement, StateData


# ---------------------------- Selection functions ----------------------------------------------------

def Pinj(measurement, hDataDict, Ybus, hValues, gridTopology):
    sum  = 0.0
    Vi = hValues[hDataDict['v'+str(measurement.bus[0])].index]

    angles = np.zeros(2)
    if measurement.bus[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(measurement.bus[0])].index]

    for key in gridTopology.keys():
        Voltages = Vi*hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
        
        rightSide = Ybus[measurement.bus[0]-1, key-1].real*math.cos(angles[0]-angles[1]) + Ybus[measurement.bus[0]-1, key-1].imag*math.sin(angles[0]-angles[1])

        sum += Voltages*rightSide

    return sum

def Qinj(measurement, hDataDict, Ybus, hValues, gridTopology):
    sum  = 0.0
    Vi = hValues[hDataDict['v'+str(measurement.bus[0])].index]

    angles = np.zeros(2)
    if measurement.bus[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(measurement.bus[0])].index]

    for key in gridTopology.keys():
        Voltages = Vi*hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
        
        rightSide = Ybus[measurement.bus[0]-1, key-1].real*math.sin(angles[0]-angles[1]) - Ybus[measurement.bus[0]-1, key-1].imag*math.cos(angles[0]-angles[1])

        sum += Voltages*rightSide

    return sum


def Pflow(measurement, hDataDict, Ybus, hValues, *args):
    angles = np.zeros(2)
    voltages = np.ones(2)

    for i in range(len(measurement.bus)):
        if measurement.bus[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(measurement.bus[i])].index]

        voltages[i] = hValues[hDataDict['v'+str(measurement.bus[i])].index]


    leftside = -voltages[0]*voltages[0]*(Ybus[measurement.bus[0]-1, measurement.bus[1]-1].real) 
    rightSide = voltages[0]*voltages[1]*(Ybus[measurement.bus[0]-1, measurement.bus[1]-1].real*math.cos(angles[0]-angles[1]) + Ybus[measurement.bus[0]-1, measurement.bus[1]-1].imag*math.sin(angles[0]-angles[1]))

    return leftside + rightSide


def Qflow(measurement, hDataDict, Ybus, hValues, *args):
    angles = np.zeros(2)
    voltages = np.ones(2)

    for i in range(len(measurement.bus)):
        if measurement.bus[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(measurement.bus[i])].index]

        voltages[i] = hValues[hDataDict['v'+str(measurement.bus[i])].index]


    leftside = voltages[0]*voltages[0]*(Ybus[measurement.bus[0]-1, measurement.bus[1]-1].imag) 
    rightSide = voltages[0]*voltages[1]*(Ybus[measurement.bus[0]-1, measurement.bus[1]-1].real*math.sin(angles[0]-angles[1]) - Ybus[measurement.bus[0]-1, measurement.bus[1]-1].imag*math.cos(angles[0]-angles[1]))

    return leftside + rightSide


def Vmag(measurement, hDataDict, Ybus, hValues, *args):
    return hValues[hDataDict['v'+str(measurement.bus[0])].index]


def Iflow(measurement, hDataDict, Ybus, *args):
    return 0.0

def stateFunctionCalculator(measurementDict, hDataDict, Ybus, hValues, gridTopology):
    stateFunction = np.zeros(len(measurementDict), dtype=float)
    
    calcSelector = {
        0: Pinj,
        1: Qinj,
        2: Pflow,
        3: Qflow,
        4: Vmag,
        5: Iflow
    }
    
    for i, (key, measurement) in enumerate(measurementDict.items()):
        stateFunction[i]=calcSelector[measurement.category](measurement, hDataDict, Ybus, hValues, gridTopology)
    
    return stateFunction

def CostCalculator(measurementDict, hDataDict, Ybus, hValues, gridTopology):
    cost = 0.0
    stateFunction = stateFunctionCalculator(measurementDict, hDataDict, Ybus, hValues, gridTopology)
    
    for i, (key, measurement) in enumerate(measurementDict.items()):
        cost+=((measurement.value-stateFunction[i])**2)/measurement.covariance
    
    return cost
    

# ------------------- GMatrixCalculator -----------------------------------------------------------

def GMatrixCalculator(jacobian, measurementDict, hDataDict, Ybus, hValues, gridTopology):
    covarianceMatrix = np.zeros((len(measurementDict), len(measurementDict)))
    stateDifferenceT = np.zeros((len(measurementDict)), dtype=float)

    calcSelector = {
        0: Pinj,
        1: Qinj,
        2: Pflow,
        3: Qflow,
        4: Vmag,
        5: Iflow
    }


    for i, (key, measurement) in enumerate(measurementDict.items()):
        covarianceMatrix[i,i] = measurement.covariance
        state=calcSelector[measurement.category](measurement, hDataDict, Ybus, hValues, gridTopology)
        stateDifferenceT[i] = measurement.value - state

    print(f'state={stateDifferenceT}')
    
    jacobianT = np.transpose(jacobian)
    stateDifference = np.transpose(stateDifferenceT)
    covarianceMatrixInv = np.linalg.inv(covarianceMatrix)


    HtR = jacobianT@covarianceMatrixInv
    gainMatrix = HtR@jacobian

    yMatrix =  HtR@stateDifference

    gainShape = gainMatrix.shape

    for i in range(gainShape[0]):
        for j in range(gainShape[1]):
            if abs(gainMatrix[i,j]) < 0.000001:
                gainMatrix[i,j] = 0.0


    return gainMatrix, yMatrix



def CalculateEstimatedValues(measurementDict, hDataDict, Ybus, hValues, gridTopology):
    residuals = np.zeros(len(measurementDict), dtype=float)
    
    estimatedValues = stateFunctionCalculator(measurementDict, hDataDict, Ybus, hValues, gridTopology)
    
    for i, measurement in enumerate(measurementDict.values()):
        residuals[i]=measurement.value - estimatedValues[i]
        
    
    return [estimatedValues, residuals]