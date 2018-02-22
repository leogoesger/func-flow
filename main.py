from utils.helpers import create_folders, get_calculation_numbers
from calculations.WinterHighflow import WinterHighflowPOR, WinterHighflow
from calculations.SpringTransition import SpringTransition
from calculations.SummerBaseflow import SummerBaseflow
from calculations.FallFlush import FallFlush
from calculations.FallWinterBaseflow import FallWinterBaseflow
from calculations.AllYear import AllYear
from calculations.AnnualFlowMatrix import AnnualFlowMatrix

directory_name = 'rawFiles'
end_with = '.csv'

create_folders()
calculation_number, start_date, class_number, gauge_numbers = get_calculation_numbers()

if calculation_number == 1:
    print('Calculating Annual Winter Highflow properties with start date at {} in {} directory'.format(start_date, directory_name))
    WinterHighflow(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 2:
    print('Calculating Spring Transition properties with start date at {} in {} directory'.format(start_date, directory_name))
    SpringTransition(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 3:
    print('Calculating Start of Summer properties with start date at {} in {} directory'.format(start_date, directory_name))
    SummerBaseflow(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 4:
    print('Calculating Fall Flush properties with start date at {} in {} directory'.format(start_date, directory_name))
    FallFlush(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 5:
    print('Calculating Fall Winter Baseflow properties with start date at {} in {} directory'.format(start_date, directory_name))
    FallWinterBaseflow(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 6:
    print('Calculating All Year properties with start date at {} in {} directory'.format(start_date, directory_name))
    AllYear(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()
elif calculation_number == 7:
    print('Calculating Annual Flow Metrics with start date at {} in {} directory'.format(start_date, directory_name))
    AnnualFlowMatrix(start_date, directory_name, end_with, class_number, gauge_numbers).calculate()
elif calculation_number == 8:
    print('Calculating Winter Highflow POR with start date at {} in {} directory'.format(start_date, directory_name))
    WinterHighflowPOR(start_date, directory_name, end_with, class_number, gauge_numbers, True).calculate()

print('')
print('Done!!!!!!!!!!!!!!!!')
