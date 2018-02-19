from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.AnnualFlowMatrix import AnnualFlowMatrix

start_date = '10/1'
directory_name = 'tests/testFiles'
end_with = 'Case_1.csv'
class_number = 3
gauge_numbers = [11475560]

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Annual Flow matrix calculation')
AnnualFlowMatrix(start_date, directory_name, end_with, class_number, None).calculate()
AnnualFlowMatrix(start_date, directory_name, end_with, None, gauge_numbers).calculate()
AnnualFlowMatrix(start_date, directory_name, end_with, None, None).calculate()
