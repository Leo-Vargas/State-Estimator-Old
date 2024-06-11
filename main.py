import numpy as np
from classes import Measurement, StateData
from functions import hSetup, hDataDictUpdate, PrintStateData, PrintEstimatedValuesData, createGridTopology
from JacobianCalculator import JacobianCalculator
from Gmatrix import GMatrixCalculator, CostCalculator, CalculateEstimatedValues 

# --------------- entry data ---------------
measurementDict = {
    'p12': Measurement(2, (1, 2), 0.888, 0.008**2),
    'p13': Measurement(2, (1, 3), 1.173, 0.008**2),
    'p2': Measurement(0, (2,), -0.501, 0.01**2),
    'q12': Measurement(3, (1, 2), 0.568, 0.008**2),
    'q13': Measurement(3, (1, 3), 0.663, 0.008**2),
    'q2': Measurement(1, (2,), -0.286, 0.01**2),
    'v1': Measurement(4, (1,), 1.006, 0.004**2),
    'v2': Measurement(4, (2,), 0.968, 0.004**2)
}

Ybus = np.array([
    (16.89655172414-47.2413793103j, -10.+30.j, -6.896551172414+17.2413793103j),
    (-10.+30.j, 14.1095890411-40.9589041096j, -4.1095890411+10.9589041096j),
    (-6.896551172414+17.2413793103j, -4.1095890411+10.9589041096j, 11.0061407652-28.2002834199j)
])

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

