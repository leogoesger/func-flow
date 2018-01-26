from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from calculations.coefficient_of_variance import coefficient_of_variance

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbe = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('COV calculation')
coefficient_of_variance(start_date, directoryName, endWith)
