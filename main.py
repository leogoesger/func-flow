from calculations.coefficient_of_variance import coefficient_of_variance
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from calculations.exceedance import exceedance
from calculations.start_of_summer import start_of_summer
from calculations.timing_duration_frequency import timing_duration_frequency

calculation_number = None

if not calculation_number:
    calculation_number = int(input('Select the Following Calculations:\n 1. Average, Standard Deviation, Coefficient of Variance and Plots\n 2. Dim hydrograph plotter\n 3. 2%, 5%, 10%, 20% and 50% Exceedance\n 4. Start of Summer\n 5. Timing, Duration and Frequence\n'))

start_date = input('Start Date of each water year? Default: 10/1 =>')
if not start_date:
    start_date = '10/1'
directoryName = input('Directory Path? Default: rawFiles =>')
if not directoryName:
    directoryName = 'rawFiles'
endWith = input('File name end with? Default: .csv =>')
if not endWith:
    endWith = '.csv'


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
    print('Calculating Timing Duration and Frequence with start date at {} in {} directory'.format(start_date, directoryName))
    timing_duration_frequency(start_date, directoryName, endWith)
