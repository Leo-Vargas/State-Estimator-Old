import numpy as np

from classes import Measurement
from cases import SelectCase
from functions import hSetup, hDataDictUpdate, PrintStateData, PrintEstimatedValuesData, createGridTopology
from JacobianCalculator import JacobianCalculator
from Gmatrix import GMatrixCalculator, CostCalculator, CalculateEstimatedValues 

# --------------- entry data ---------------
[measurementDict, Ybus] = SelectCase('Exposit3Bus')
gridTopology = createGridTopology(Ybus)

# --------------- First Iteration Setup ---------------
np.set_printoptions(precision=4)
[hValues, hDataDict] = hSetup(gridTopology)
deltaStates = np.ones(len(hValues))
stopCondition = 0.0001
iteration = 0
while any( abs(deltaState) > stopCondition for deltaState in deltaStates):

    iteration+=1
    print('\n\n')
    print('#######################################################')
    print(f'######------------ {iteration} iteration start ------------######' )
    print('\n')

    jacobian = JacobianCalculator(list(measurementDict.values()), hDataDict, Ybus, hValues, gridTopology)
    print(f'------------- jacobian: iteration {iteration} ------------------')
    print(jacobian)
    print('\n')

    [gainMatrix, yMatrix] = GMatrixCalculator(jacobian, measurementDict, hDataDict, Ybus, hValues, gridTopology)
    print(f'------------------- gain matrix: iteration {iteration} ----------------------')
    print(gainMatrix)
    print('\n')

    print(f'--------------Y vectors: iteration {iteration} -------------------')
    print(yMatrix)
    print('\n')


    deltaStates = np.linalg.solve(gainMatrix, yMatrix)
    cost = CostCalculator(measurementDict, hDataDict, Ybus, hValues, gridTopology)
    print(f'--------------Delta States: iteration {iteration} ------------------')
    print(deltaStates)
    print('Total cost: ' + str(cost))
    print('\n')
    
    
    hValues+=deltaStates
    print(f'hvalues={hValues}')
    hDataDictUpdate(hValues, hDataDict)


else:
    print('\n\n')
    print('#######################################################')
    print(f'####------------ algorithm ended on {iteration} iterations ------------####' )
    print('Results are as followed:')
    print('\n')
    
    print('---------------------- State Values ---------------------')
    PrintStateData(hDataDict)
    
    
    print('---------------------- Estimated Values ---------------------')
    [estimatedValues, residuals] = CalculateEstimatedValues(measurementDict, hDataDict, Ybus, hValues, gridTopology)
    PrintEstimatedValuesData(measurementDict, estimatedValues, residuals)

