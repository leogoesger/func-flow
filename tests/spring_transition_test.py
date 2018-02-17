from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.spring_transition import spring_transition

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbers = [11475560]

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Fall Flush calculation')
spring_transition(start_date, directoryName, endWith, class_number, None, False)
spring_transition(start_date, directoryName, endWith, None, gauge_numbers, False)
spring_transition(start_date, directoryName, endWith, None, None, False)
