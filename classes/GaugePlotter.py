import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

class GaugePlotter:

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
