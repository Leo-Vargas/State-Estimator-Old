import numpy as np
import math
from classes import Measurement, StateData

def PinjCalculatorAngleSame(hValues, hDataDict, Ybus, buses, gridTopology):
    
    sum = 0.0
    Vi = hValues[hDataDict['v'+str(buses[0])].index]
    weight = (Vi*Vi*Ybus[buses[0]-1, buses[0]-1].imag)
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    for key in gridTopology.keys():
        Voltages = Vi*hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
                
        rightSide = -Ybus[buses[0]-1, key-1].real*math.sin(angles[0]-angles[1]) + Ybus[buses[0]-1, key-1].imag*math.cos(angles[0]-angles[1])
            
        sum += Voltages*rightSide            
    
    return sum - weight

def PinjCalculatorAngleDiff(hValues, hDataDict, Ybus, buses, hData):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]*hValues[hDataDict['v'+str(hData.bus)].index]
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    angles[1] = hValues[hData.index]
    
    rightSide = Ybus[buses[0]-1, hData.bus-1].real*math.sin(angles[0]-angles[1]) - Ybus[buses[0]-1, hData.bus-1].imag*math.cos(angles[0]-angles[1])  
  
    return Voltages*rightSide

def PinjCalculatorVoltageSame(hValues, hDataDict, Ybus, buses, gridTopology):
    sum = 0.0
    Vi = hValues[hDataDict['v'+str(buses[0])].index]
    weight = (Vi*Ybus[buses[0]-1, buses[0]-1].real)
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    for key in gridTopology.keys():
        Voltages = hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
                
        rightSide = Ybus[buses[0]-1, key-1].real*math.cos(angles[0]-angles[1]) + Ybus[buses[0]-1, key-1].imag*math.sin(angles[0]-angles[1])
            
        sum += Voltages*rightSide            
    
    return sum + weight

def PinjCalculatorVoltageDiff(hValues, hDataDict, Ybus, buses, hData):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    if hData.bus == 1:
        angles[1] = 0.0
    else:
        angles[1] = hValues[hDataDict['a'+str(hData.bus)].index]
    
    rightSide = Ybus[buses[0]-1, hData.bus-1].real*math.cos(angles[0]-angles[1]) + Ybus[buses[0]-1, hData.bus-1].imag*math.sin(angles[0]-angles[1])  
    
    return Voltages*rightSide


def QinjCalculatorAngleSame(hValues, hDataDict, Ybus, buses, gridTopology):
    
    sum = 0.0
    Vi = hValues[hDataDict['v'+str(buses[0])].index]
    weight = (Vi*Vi*Ybus[buses[0]-1, buses[0]-1].real)
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    for key in gridTopology.keys(): 
        Voltages = Vi*hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
                
        rightSide = Ybus[buses[0]-1, key-1].real*math.cos(angles[0]-angles[1]) + Ybus[buses[0]-1, key-1].imag*math.sin(angles[0]-angles[1])
            
        sum += Voltages*rightSide         
    
    return sum - weight

def QinjCalculatorAngleDiff(hValues, hDataDict, Ybus, buses, hData):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]*hValues[hDataDict['v'+str(hData.bus)].index]
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    angles[1] = hValues[hData.index]
    
    rightSide = - Ybus[buses[0]-1, hData.bus-1].real*math.cos(angles[0]-angles[1]) - Ybus[buses[0]-1, hData.bus-1].imag*math.sin(angles[0]-angles[1])  
  
    return Voltages*rightSide

def QinjCalculatorVoltageSame(hValues, hDataDict, Ybus, buses, gridTopology):
    sum = 0.0
    Vi = hValues[hDataDict['v'+str(buses[0])].index]
    weight = (Vi*Ybus[buses[0]-1, buses[0]-1].imag)
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    for key in gridTopology.keys():
        Voltages = hValues[hDataDict['v'+str(key)].index]
            
        if key == 1:
            angles[1] = 0.0
        else:
            angles[1] = hValues[hDataDict['a'+str(key)].index]
                
        rightSide = Ybus[buses[0]-1, key-1].real*math.sin(angles[0]-angles[1]) - Ybus[buses[0]-1, key-1].imag*math.cos(angles[0]-angles[1])
            
        sum += Voltages*rightSide 
            
    return sum - weight

def QinjCalculatorVoltageDiff(hValues, hDataDict, Ybus, buses, hData):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]
    
    angles = np.zeros(2)
    if buses[0] == 1:
        angles[0] = 0.0
    else:
        angles[0] = hValues[hDataDict['a'+str(buses[0])].index]
    
    if hData.bus == 1:
        angles[1] = 0.0
    else:
        angles[1] = hValues[hDataDict['a'+str(hData.bus)].index]
    
    rightSide = Ybus[buses[0]-1, hData.bus-1].real*math.sin(angles[0]-angles[1]) - Ybus[buses[0]-1, hData.bus-1].imag*math.cos(angles[0]-angles[1])  
    
    return Voltages*rightSide


def PflowCalculatorAngle(hValues, hDataDict, Ybus, buses):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]*hValues[hDataDict['v'+str(buses[1])].index]

    angles = np.zeros(len(buses))
    for i in range(len(buses)):    
        if buses[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(buses[i])].index]
    
    rightSide = -Ybus[buses[0]-1, buses[1]-1].real*math.sin(angles[0]-angles[1]) + Ybus[buses[0]-1, buses[1]-1].imag*math.cos(angles[0]-angles[1])    
    print(f'rightSidePF: {-Ybus[buses[0]-1, buses[1]-1].real*math.sin(angles[0]-angles[1])} + {Ybus[buses[0]-1, buses[1]-1].imag*math.cos(angles[0]-angles[1])} = {rightSide}')

    return Voltages*rightSide

def PflowCalculatorVoltage(hValues, hDataDict, Ybus, buses, Vindex):

    Voltages = hValues[Vindex]

    angles = np.zeros(len(buses))
    for i in range(len(buses)):    
        if buses[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(buses[i])].index]
    
    rightSide = -Ybus[buses[0]-1, buses[1]-1].real*math.cos(angles[0]-angles[1]) - Ybus[buses[0]-1, buses[1]-1].imag*math.sin(angles[0]-angles[1])    
    
    return Voltages*rightSide


def QflowCalculatorAngle(hValues, hDataDict, Ybus, buses):
    
    Voltages = hValues[hDataDict['v'+str(buses[0])].index]*hValues[hDataDict['v'+str(buses[1])].index]

    angles = np.zeros(len(buses))
    for i in range(len(buses)):    
        if buses[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(buses[i])].index]
    
    rightSide = -Ybus[buses[0]-1, buses[1]-1].real*math.cos(angles[0]-angles[1]) - Ybus[buses[0]-1, buses[1]-1].imag*math.sin(angles[0]-angles[1])    
    
    return Voltages*rightSide

def QflowCalculatorVoltage(hValues, hDataDict, Ybus, buses, Vindex):

    Voltages = hValues[Vindex]

    angles = np.zeros(len(buses))
    for i in range(len(buses)):    
        if buses[i] == 1:
            angles[i] = 0.0
        else:
            angles[i] = hValues[hDataDict['a'+str(buses[i])].index]
    
    rightSide = -Ybus[buses[0]-1, buses[1]-1].real*math.sin(angles[0]-angles[1]) + Ybus[buses[0]-1, buses[1]-1].imag*math.cos(angles[0]-angles[1])    
    
    return Voltages*rightSide


# ------------------------ JacobianCalculator related functions ------------------------------------

def Pinj(measurement, hDataDict, Ybus, hValues, gridTopology):
    jacobianRow = np.zeros(len(hDataDict))
    
    
    for i, (key, hData) in enumerate(hDataDict.items()):
        if hData.category == 0:
            if measurement.bus[0] == hData.bus:
                jacobianRow[i]=PinjCalculatorAngleSame(hValues, hDataDict, Ybus, measurement.bus, gridTopology)
            
            else:
                jacobianRow[i]=PinjCalculatorAngleDiff(hValues, hDataDict, Ybus, measurement.bus, hData)
                

        elif hData.category == 1:
            if measurement.bus[0] == hData.bus:
                jacobianRow[i]=PinjCalculatorVoltageSame(hValues, hDataDict, Ybus, measurement.bus, gridTopology)
                
            else:
                jacobianRow[i]=PinjCalculatorVoltageDiff(hValues, hDataDict, Ybus, measurement.bus, hData)    
    
    return jacobianRow


def Qinj(measurement, hDataDict, Ybus, hValues, gridTopology):
    jacobianRow = np.zeros(len(hDataDict))
    
    
    for i, (key, hData) in enumerate(hDataDict.items()):
        if hData.category == 0:
            if measurement.bus[0] == hData.bus:
                jacobianRow[i]=QinjCalculatorAngleSame(hValues, hDataDict, Ybus, measurement.bus, gridTopology)
            
            else:
                jacobianRow[i]=QinjCalculatorAngleDiff(hValues, hDataDict, Ybus, measurement.bus, hData)
                

        elif hData.category == 1:
            if measurement.bus[0] == hData.bus:
                jacobianRow[i]=QinjCalculatorVoltageSame(hValues, hDataDict, Ybus, measurement.bus, gridTopology)
                
            else:
                jacobianRow[i]=QinjCalculatorVoltageDiff(hValues, hDataDict, Ybus, measurement.bus, hData)    
    
    return jacobianRow


def Pflow(measurement, hDataDict, Ybus, hValues, *args):
    jacobianRow = np.zeros((len(hDataDict)), dtype=float)
    

    for i, (key, hData) in enumerate(hDataDict.items()):
        if hData.category == 0:
            if measurement.bus[0] != hData.bus and measurement.bus[1] != hData.bus:
                jacobianRow[i]=0.0

            elif measurement.bus[0] == hData.bus:
                jacobianRow[i]=PflowCalculatorAngle(hValues, hDataDict, Ybus, measurement.bus)
            
            elif measurement.bus[1] == hData.bus:
                jacobianRow[i]=-PflowCalculatorAngle(hValues, hDataDict, Ybus, measurement.bus)
                

        elif hData.category == 1:
            if measurement.bus[0] != hData.bus and measurement.bus[1] != hData.bus:
                jacobianRow[i]=0.0
                
            elif measurement.bus[0] == hData.bus:
                jacobianRow[i]=-PflowCalculatorVoltage(hValues, hDataDict, Ybus, measurement.bus, hDataDict['v'+str(measurement.bus[1])].index) - 2*Ybus[measurement.bus[0]-1, measurement.bus[1]-1].real*hValues[hData.index]
                
            elif measurement.bus[1] == hData.bus:
                jacobianRow[i]=-PflowCalculatorVoltage(hValues, hDataDict, Ybus, measurement.bus, hDataDict['v'+str(measurement.bus[0])].index)          

    return jacobianRow


def Qflow(measurement, hDataDict, Ybus, hValues, *args):
    jacobianRow = np.zeros((len(hDataDict)), dtype=float)
    

    for i, (key, hData) in enumerate(hDataDict.items()):
        if hData.category == 0:
            if measurement.bus[0] != hData.bus and measurement.bus[1] != hData.bus:
                jacobianRow[i]=0.0

            elif measurement.bus[0] == hData.bus:
                jacobianRow[i]=-QflowCalculatorAngle(hValues, hDataDict, Ybus, measurement.bus)
            
            elif measurement.bus[1] == hData.bus:
                jacobianRow[i]=QflowCalculatorAngle(hValues, hDataDict, Ybus, measurement.bus)
                

        elif hData.category == 1:
            if measurement.bus[0] != hData.bus and measurement.bus[1] != hData.bus:
                jacobianRow[i]=0.0
                
            elif measurement.bus[0] == hData.bus:
                jacobianRow[i]=-QflowCalculatorVoltage(hValues, hDataDict, Ybus, measurement.bus, hDataDict['v'+str(measurement.bus[1])].index) + 2*Ybus[measurement.bus[0]-1, measurement.bus[1]-1].imag*hValues[hData.index]
                
            elif measurement.bus[1] == hData.bus:
                jacobianRow[i]=-QflowCalculatorVoltage(hValues, hDataDict, Ybus, measurement.bus, hDataDict['v'+str(measurement.bus[0])].index) 
                

    return jacobianRow


def Vmag(measurement, hDataDict, *args):
    jacobianRow = np.zeros((len(hDataDict)), dtype=float)
    
    for i, (key, hData) in enumerate(hDataDict.items()):
        if hData.category == 1 and hData.bus == measurement.bus[0]:
            jacobianRow[i] = 1.0
    return jacobianRow


def Iflow(measurement, hDataDict, Ybus, *args):
    jacobianRow = np.zeros((len(hDataDict)), dtype=float)
    return jacobianRow
   

def JacobianCalculator(measurementList: list, hDataDict: dict, Ybus: np.ndarray, hValues: np.ndarray, gridTopology: dict):
    
    jacobian = np.zeros((len(measurementList), len(hValues)), dtype=float)
    
    
    calcSelector = {
        0: Pinj,
        1: Qinj,
        2: Pflow,
        3: Qflow,
        4: Vmag,
        5: Iflow
    }
    
    for j in range(len(measurementList)):
        jacobian[j]=calcSelector[measurementList[j].category](measurementList[j], hDataDict, Ybus, hValues, gridTopology)
            
    
    return jacobian