from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from calculations.winter_highflow_properties_POR import timing_duration_frequency_POR

start_date = '10/1'
directoryName = 'tests/testFiles'
endWith = 'Case_1.csv'
class_number = 3
gauge_numbe = 11475560

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow Singular Single Gauge calculation')
timing_duration_frequency_POR(start_date, directoryName, endWith, None, gauge_numbe)
