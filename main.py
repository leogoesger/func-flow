from calculations.coefficient_of_variance import coefficient_of_variance
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from calculations.exceedance import exceedance
from calculations.start_of_summer import start_of_summer
from calculations.winter_highflow_properties_singular import timing_duration_frequency_singular
from calculations.winter_highflow_properties import timing_duration_frequency

from pre_processFiles.gauge_reference import new_gauges

calculation_number = None

while not calculation_number:
    calculation_number = int(input('Select the Following Calculations:\n 1. Average, Standard Deviation, Coefficient of Variance and Plots\n 2. Dim hydrograph plotter\n 3. 2%, 5%, 10%, 20% and 50% Exceedance\n 4. Start of Summer\n 5. Winter Highflow Properties \n 6. Winter Highflow Properties for Single Gauge\n'))

start_date = input('Start Date of each water year? Default: 10/1 => ')
if not start_date:
    start_date = '10/1'

directoryName = 'testFiles'
endWith = '5.csv'

if calculation_number == 1:
    print('Calculating Coefficient of Variance with start date at {} in {} directory'.format(start_date, directoryName))
    coefficient_of_variance(start_date, directoryName, endWith)
elif calculation_number == 2:
    print('Calculating Dimensionless Hydrograph with start date at {} in {} directory'.format(start_date, directoryName))
    dim_hydrograph_plotter(start_date, directoryName, endWith)
elif calculation_number == 3:
    print('Calculating Exceedance Rate with start date at {} in {} directory'.format(start_date, directoryName))
    exceedance(start_date, directoryName, endWith)
elif calculation_number == 4:
    print('Calculating Start of Summer with start date at {} in {} directory'.format(start_date, directoryName))
    start_of_summer(start_date, directoryName, endWith)
elif calculation_number == 5:
    print('Calculating Winter Highflow\'s Timing Duration and Frequence with start date at {} in {} directory'.format(start_date, directoryName))
    timing_duration_frequency(start_date, directoryName, endWith)
elif calculation_number == 6:
    method = input('Type 1 for calculating the entire Class, 2 for a single Gauge =>  ')
    if int(method) == 1:
        class_number = input('Class Number? => ')
        if int(class_number) <= 9:
            timing_duration_frequency_singular(start_date, directoryName, endWith, class_number, None)
        else:
            print('What?')
    elif int(method) == 2:
        gauge_number = input('Gauge Number? => ')
        if int(gauge_number) in new_gauges:
            timing_duration_frequency_singular(start_date, directoryName, endWith, None, gauge_number)
        else:
            print('Could not find Gauge number!')
    else:
        print('What the heck was that?')
else:
    print('What the heck was that?')
