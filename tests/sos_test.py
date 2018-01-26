from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from calculations.start_of_summer import start_of_summer

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbe = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Start of Summer calculation')
start_of_summer(start_date, directoryName, endWith)
