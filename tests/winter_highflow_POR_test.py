from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.winter_highflow import winter_highflow_POR

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_number = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow POR calculation')
winter_highflow_POR(start_date, directoryName, endWith, class_number, None, False)
winter_highflow_POR(start_date, directoryName, endWith, None, gauge_number, False)
winter_highflow_POR(start_date, directoryName, endWith, None, None, False)
