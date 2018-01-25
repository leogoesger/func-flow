from calculations.coefficient_of_variance import coefficient_of_variance
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from calculations.exceedance import exceedance
from calculations.start_of_summer import start_of_summer
from calculations.winter_highflow_properties_singular import timing_duration_frequency_singular
from calculations.winter_highflow_properties import timing_duration_frequency

start_date = '10/1'
directoryName = 'tests'
endWith = '1.csv'
class_number = 3
gauge_numbe = 11523200

print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('COV calculation')
coefficient_of_variance(start_date, directoryName, endWith)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Dim hydro graph calculation')
dim_hydrograph_plotter(start_date, directoryName, endWith)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Exceedance calculation')
exceedance(start_date, directoryName, endWith)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Start of Summer calculation')
start_of_summer(start_date, directoryName, endWith)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow Singlular Entire Class calculation')
timing_duration_frequency_singular(start_date, directoryName, endWith, class_number, None)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow Singular Single Gauge calculation')
timing_duration_frequency_singular(start_date, directoryName, endWith, None, gauge_numbe)
print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
print('Winter High Flow Properties calculation')
timing_duration_frequency(start_date, directoryName, endWith)
