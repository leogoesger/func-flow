from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from calculations.exceedance import exceedance

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbe = 11475560


print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Exceedance calculation')
exceedance(start_date, directoryName, endWith)
