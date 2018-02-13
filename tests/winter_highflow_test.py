from os import sys, path
from calculations.winter_highflow import winter_highflow_annual
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_number = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow calculation')
winter_highflow_annual(start_date, directoryName, endWith, class_number, None)
winter_highflow_annual(start_date, directoryName, endWith, None, gauge_number)
winter_highflow_annual(start_date, directoryName, endWith, None, None)
