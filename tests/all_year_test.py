from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.all_year import all_year
from utils.helpers import create_folders

create_folders()

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_number = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('All Year calculation')
all_year(start_date, directoryName, endWith, class_number, None)
all_year(start_date, directoryName, endWith, None, gauge_number)
