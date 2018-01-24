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


coefficient_of_variance(start_date, directoryName, endWith)
dim_hydrograph_plotter(start_date, directoryName, endWith)
exceedance(start_date, directoryName, endWith)
start_of_summer(start_date, directoryName, endWith)
timing_duration_frequency_singular(start_date, directoryName, endWith, class_number, None)
timing_duration_frequency_singular(start_date, directoryName, endWith, None, gauge_numbe)
timing_duration_frequency(start_date, directoryName, endWith)
