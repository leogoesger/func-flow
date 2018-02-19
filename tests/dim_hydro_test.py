from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter

start_date = '10/1'
directory_name = 'tests/testFiles'
end_with = 'Case_1.csv'
class_number = 3
gauge_numbers = [11475560]

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Dim hydro graph calculation')
dim_hydrograph_plotter(start_date, directory_name, end_with, None, gauge_numbers, False)
dim_hydrograph_plotter(start_date, directory_name, end_with, class_number, None, False)
dim_hydrograph_plotter(start_date, directory_name, end_with, None, None, False)
