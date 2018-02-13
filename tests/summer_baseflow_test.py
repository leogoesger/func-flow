from os import sys, path
from calculations.summer_baseflow import summer_baseflow
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_number = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Start of Summer calculation')
summer_baseflow(start_date, directoryName, endWith, None, gauge_number)
summer_baseflow(start_date, directoryName, endWith, class_number, None)
summer_baseflow(start_date, directoryName, endWith, None, None)
