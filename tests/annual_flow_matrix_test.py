from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.annual_flow_matrix import annual_flow_matrix

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbers = [11475560]

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Annual Flow matrix calculation')
annual_flow_matrix(start_date, directoryName, endWith, class_number, None)
annual_flow_matrix(start_date, directoryName, endWith, None, gauge_numbers)
annual_flow_matrix(start_date, directoryName, endWith, None, None)
