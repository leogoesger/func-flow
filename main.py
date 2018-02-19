from utils.helpers import create_folders, get_calculation_numbers
from calculations.winter_highflow import winter_highflow_POR, winter_highflow_annual
from calculations.spring_transition import spring_transition
from calculations.summer_baseflow import summer_baseflow
from calculations.fall_flush import fall_flush
from calculations.fall_winter_baseflow import fall_winter_baseflow
from calculations.dim_hydrograph_plotter import dim_hydrograph_plotter
from calculations.AllYear import AllYear
from calculations.AnnualFlowMatrix import AnnualFlowMatrix

directory_name = 'rawFiles'
end_with = '.csv'

create_folders()
calculation_number, start_date, class_number, gauge_numbers = get_calculation_numbers()

if calculation_number == 1:
    print('Calculating Annual Winter Highflow properties with start date at {} in {} directory'.format(start_date, directory_name))
    winter_highflow_annual(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 2:
    print('Calculating Spring Transition properties with start date at {} in {} directory'.format(start_date, directory_name))
    spring_transition(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 3:
    print('Calculating Start of Summer properties with start date at {} in {} directory'.format(start_date, directory_name))
    summer_baseflow(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 4:
    print('Calculating Fall Flush properties with start date at {} in {} directory'.format(start_date, directory_name))
    fall_flush(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 5:
    print('Calculating Fall Winter Baseflow properties with start date at {} in {} directory'.format(start_date, directory_name))
    fall_winter_baseflow(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 6:
    print('Calculating All Year properties with start date at {} in {} directory'.format(start_date, directory_name))
    AllYear(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 7:
    print('Calculating Annual Flow Metrics with start date at {} in {} directory'.format(start_date, directory_name))
    AnnualFlowMatrix(start_date, directory_name, end_with, class_number, gauge_numbers).calculate()
elif calculation_number == 8:
    print('Calculating Dimensionless Hydrograph with start date at {} in {} directory'.format(start_date, directory_name))
    dim_hydrograph_plotter(start_date, directory_name, end_with, class_number, gauge_numbers, True)
elif calculation_number == 9:
    print('Calculating Winter Highflow POR with start date at {} in {} directory'.format(start_date, directory_name))
    winter_highflow_POR(start_date, directory_name, end_with, class_number, gauge_numbers, True)

print('')
print('Done!!!!!!!!!!!!!!!!')
