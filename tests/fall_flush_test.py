from os import sys, path
from calculations.fall_flush import fall_flush
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_number = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Fall Flush calculation')
fall_flush(start_date, directoryName, endWith, class_number, None)
fall_flush(start_date, directoryName, endWith, None, gauge_number)
fall_flush(start_date, directoryName, endWith, None, None)
