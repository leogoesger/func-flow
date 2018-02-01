import os
from calculations.annual_flow_matrix import annual_flow_matrix
from calculations.coefficient_of_variance import coefficient_of_variance
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from calculations.exceedance import exceedance
from calculations.spring_transition import spring_transition
from calculations.summer_baseflow import start_of_summer
from calculations.winter_highflow_properties_POR import timing_duration_frequency_POR
from calculations.winter_highflow_properties_annual import timing_duration_frequency_annual

from pre_processFiles.gauge_reference import noelle_gauges

calculation_number = None

directoryName = 'rawFiles'
endWith = '.csv'

# spring_transition()
while not calculation_number:
    print('')
    print('Select the Following Calculations: :rocket: :rocket: :rocket: :rocket:')
    calculation_number = int(input(' 1. Average, Standard Deviation, Coefficient of Variance and Plots\n 2. Dim hydrograph plotter\n 3. 2%, 5%, 10%, 20% and 50% Exceedance\n 4. Start of Summer\n 5. Annual Winter Highflow Properties \n 6. Winter Highflow Properties for POR \n 7. Annual Flow Metrics => '))

if calculation_number > 7:
    print('')
    print('What did you just do?')
    os._exit(0)

start_date = input('Start Date of each water year? Default: 10/1 => ')
if not start_date:
    start_date = '10/1'

gauge_or_class = int(input('Input 1 to calculate entire Class, 2 for single Gauge, or 3 for All Gauges=> '))
if gauge_or_class == 1:
    gauge_number = None
    class_number = input('Class Number? Default: 3 => ')
    if not class_number:
        class_number = 3
    class_number = int(class_number)
elif gauge_or_class == 2:
    class_number = None
    gauge_number = input('Gauge Number? Default: 11237500 => ')
    if not gauge_number:
        gauge_number = 11237500
    if not int(gauge_number) in noelle_gauges:
        print('')
        print('What did you just do?')
        os._exit(0)
    gauge_number = int(gauge_number)
elif gauge_or_class == 3:
    class_number = None;
    gauge_number = None;
else:
    print('')
    print('Something went wrong there!')


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
    start_of_summer(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 5:
    print('Calculating Annual Winter Highflow\'s Timing Duration and Frequence with start date at {} in {} directory'.format(start_date, directoryName))
    timing_duration_frequency_annual(start_date, directoryName, endWith)
elif calculation_number == 6:
    print('Calculating Winter Highflow\'s Timing Duration and Frequence POR with start date at {} in {} directory'.format(start_date, directoryName))
    timing_duration_frequency_POR(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 7:
    print('Calculating Annual Flow Metrics with start date at {} in {} directory'.format(start_date, directoryName))
    annual_flow_matrix(start_date, directoryName, endWith, class_number, gauge_number)

print('')
print('Done!!!!!!!!!!!!!!!!')
