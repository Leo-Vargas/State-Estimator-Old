import numpy as np

from classes import Measurement

def SelectCase(case: str):

    caseSelector = {
        'Exposit3Bus': Exposito3Bus,
    }

    [measurementDict, Ybus] = caseSelector[case]()

    return [measurementDict, Ybus]

def Exposito3Bus():
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

    return [measurementDict, Ybus]