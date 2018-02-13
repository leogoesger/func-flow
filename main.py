import os
from calculations.winter_highflow import winter_highflow_POR, winter_highflow_annual
from calculations.spring_transition import spring_transition
from calculations.summer_baseflow import summer_baseflow
from calculations.fall_flush import fall_flush
from calculations.fall_winter_baseflow import fall_winter_baseflow
from calculations.all_year import all_year
from calculations.annual_flow_matrix import annual_flow_matrix
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from pre_processFiles.gauge_reference import noelle_gauges

calculation_number = None
directoryName = 'rawFiles'
endWith = '.csv'

while not calculation_number:
    print('')
    print('Select the Following Calculations:')
    calculation_number = int(input(' 1. Winter High Flow\n 2. Spring Transition\n 3. Summer Baseflow\n 4. Fall Flush \n 5. Fall Winter Baseflow \n 6. All Year \n 7. Create Annual Flow Matrix CSV \n 8. Create Dimensionless Hydrograph Plot \n 9. Annual Winter High Flow => '))

if calculation_number > 9:
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
    if int(gauge_number) not in noelle_gauges:
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
    print('Calculating Annual Winter Highflow properties with start date at {} in {} directory'.format(start_date, directoryName))
    winter_highflow_annual(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 2:
    print('Calculating Spring Transition properties with start date at {} in {} directory'.format(start_date, directoryName))
    spring_transition(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 3:
    print('Calculating Start of Summer properties with start date at {} in {} directory'.format(start_date, directoryName))
    summer_baseflow(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 4:
    print('Calculating Fall Flush properties with start date at {} in {} directory'.format(start_date, directoryName))
    fall_flush(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 5:
    print('Calculating Fall Winter Baseflow properties with start date at {} in {} directory'.format(start_date, directoryName))
    fall_winter_baseflow(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 6:
    print('Calculating All Year properties with start date at {} in {} directory'.format(start_date, directoryName))
    all_year(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 7:
    print('Calculating Annual Flow Metrics with start date at {} in {} directory'.format(start_date, directoryName))
    annual_flow_matrix(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 8:
    print('Calculating Dimensionless Hydrograph with start date at {} in {} directory'.format(start_date, directoryName))
    dim_hydrograph_plotter(start_date, directoryName, endWith, class_number, gauge_number)
elif calculation_number == 9:
    print('Calculating Winter Highflow POR with start date at {} in {} directory'.format(start_date, directoryName))
    winter_highflow_POR(start_date, directoryName, endWith, class_number, gauge_number)

print('')
print('Done!!!!!!!!!!!!!!!!')
