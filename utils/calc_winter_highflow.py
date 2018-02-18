import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def median_of_time(lt):
    n = len(lt)
    if n < 1:
        return None
    elif n % 2 ==  1:
        return lt[n//2].start_date
    elif n == 2:
        first_date = lt[0].start_date
        second_date = lt[1].start_date
        return (first_date + second_date) / 2
    else:
        first_date = lt[n//2 - 1].start_date
        second_date = lt[n//2 + 1].start_date
        return (first_date + second_date) / 2


class FlowExceedance:

    def __init__(self, start_date, end_date, duration, exceedance):
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.flow = []
        self.exceedance = exceedance

    def add_flow(self, flow_data):
        self.flow.append(flow_data)


class GaugeInfo:

    def __init__(self, class_number, gauge_number, timing, duration, freq, mag, exceedance_percent):
        self.class_number = class_number
        self.gauge_number = gauge_number
        self.timing = timing
        self.duration = duration
        self.freq = freq
        self.mag = mag
        self.exceedance_percent = exceedance_percent

    def plot_timing(self):
        plt.figure('Timing - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))
        timing_array = []
        for percent in self.exceedance_percent:
            timing_array.append(self.timing[percent])
        plt.boxplot(timing_array)
        plt.ylim( (1, 350) )
        plt.gca().set_title('Timing - {}'.format(int(self.gauge_number)))
        plt.xticks( range(6), ('', '2%', '5%', '10%', '20%', '50%') )
        plt.savefig('post_processedFiles/Boxplots/{}_timing.png'.format(self.gauge_number))

    def plot_duration(self):
        plt.figure('Duration - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))
        duration_array=[]
        for percent in self.exceedance_percent:
            duration_array.append(self.duration[percent])
        plt.boxplot(duration_array)
        plt.gca().set_title('Duration - {}'.format(int(self.gauge_number)))
        plt.xticks( range(6), ('', '2%', '5%', '10%', '20%', '50%') )
        plt.savefig('post_processedFiles/Boxplots/{}_duration.png'.format(self.gauge_number))

    def plot_mag(self):
        fig = plt.figure('Freq - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))

        ax = fig.add_subplot(111)
        ax.set_yscale("log", nonposy='clip')
        ax.set_title('Magnitude - {}'.format(int(self.gauge_number)))
        mag_array = []
        for percent in self.exceedance_percent:
            mag_array.append(self.mag[percent])
        ax.boxplot(mag_array)
        x = range(0,6)
        label = ['0', '2%', '5%', '10%', '20%', '50%']
        ax.set_xticks(x)
        ax.set_xticklabels([i for i in label])
        fig.savefig('post_processedFiles/Boxplots/{}_mag.png'.format(self.gauge_number))

    def plot_based_on_exceedance(self):
        for percent in self.exceedance_percent:
            plt.figure('Class: {}, Gauge Number: {}, {}%'.format(self.class_number, self.gauge_number, percent))
            plt.subplot(131)
            plt.boxplot(self.timing[percent])
            plt.gca().set_title('Timing')
            plt.subplot(132)
            plt.boxplot(self.duration[percent])
            plt.gca().set_title('Duration')
            plt.subplot(133)
            plt.boxplot(self.mag[percent])
            plt.gca().set_title('Magnitude')
            plt.tight_layout()
            plt.savefig('post_processedFiles/Boxplots/{}_{}.png'.format(int(self.gauge_number), percent))


def calc_winter_highflow_annual(matrix, exceedance_percent):
    exceedance_value = {}
    freq = {}
    duration = {}
    timing = {}

    for i in exceedance_percent:
        exceedance_value[i] = np.nanpercentile(matrix, 100 - i)
        freq[i] = []
        duration[i] = []
        timing[i] = []

    for column_number, flow_column in enumerate(matrix[0]):

        exceedance_object = {}
        exceedance_duration = {}
        current_flow_object = {}

        """Init current flow object"""
        for i in exceedance_percent:
            exceedance_object[i] = []
            exceedance_duration[i] = []
            current_flow_object[i] = None

        for row_number, flow_row in enumerate(matrix[:, column_number]):

            # date = get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date)

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    current_flow_object[percent].end_date = row_number

                    exceedance_duration[percent].append(current_flow_object[percent].duration)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        exceedance_object[percent].append(FlowExceedance(row_number, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                    else:
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1

        for percent in exceedance_percent:
            freq[percent].append(len(exceedance_object[percent]))
            duration[percent].append(np.nanmedian(exceedance_duration[percent]))
            timing[percent].append(median_of_time(exceedance_object[percent]))

    return timing, duration, freq

def calc_winter_highflow_POR(matrix, exceedance_percent):

    exceedance_object = {}
    exceedance_value = {}
    current_flow_object = {}
    freq = {}
    duration = {}
    timing = {}
    magnitude = {}
    average_annual_flow = np.nanmedian(matrix)

    for i in exceedance_percent:
        exceedance_value[i] = np.nanpercentile(matrix, 100 - i)
        exceedance_object[i] = []
        current_flow_object[i] = None
        freq[i] = 0
        duration[i] = []
        timing[i] = []
        magnitude[i] = []

    for column_number, flow_column in enumerate(matrix[0]):
        for row_number, flow_row in enumerate(matrix[:, column_number]):

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    """End of a object if it falls below threshold, or end of column"""
                    current_flow_object[percent].end_date = row_number + 1
                    duration[percent].append(current_flow_object[percent].duration)
                    magnitude[percent].append(max(current_flow_object[percent].flow) / average_annual_flow)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        """Begining of a object"""
                        exceedance_object[percent].append(FlowExceedance(row_number + 1, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                        timing[percent].append(row_number + 1)
                        freq[percent] = freq[percent] + 1
                    else:
                        """Continue of a object"""
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1


    return timing, duration, freq, magnitude
