import numpy.numarray as na
from pylab import *
import abc



class CommitsChart():


    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def plot_chart(self, output_filename):
        return


class CommitsBarChart(CommitsChart):
    labels = []
    data =   []
    devs = {}
    backend = None


    def  __init__(self, backend):
       self. backend = backend


    def plot_chart(self, version_dir, output_filename):
        self.backend.create_tmp_file(version_dir)
        for dev, date in self.backend.get_parsed_commit():
            if dev in self.devs:
                self.devs[dev] += 1;
            else:
                self.devs[dev] = 1
        for label, point in self.devs.items():
            self.labels.append(label)
            self.data.append(point)
        xlocations = na.array(range(len(self.data)))*3+0.5
        width = 0.5
        bar(xlocations, self.data, width=width)
        max_bar = max(self.data)

        rcParams['font.size'] = 8
        tick = int(max_bar*0.10) or 1
        yticks(range(0, max_bar + 2*tick , tick))
        xticks(xlocations+ width/2, self.labels)
        xlim(0, xlocations[-1]+width*2)
        title("Number of commits")
        gca().get_xaxis().tick_bottom()
        gca().get_yaxis().tick_left()
        savefig(output_filename)


class CommitsTimeSeries(CommitsChart):

    backend = None
    dates = {}
    values = {}
    commits = {}
    def __init__(self, backend):
        self.backend = backend


    def plot_chart(self, version_dir, output_filename):
        self.backend.create_tmp_file(version_dir)
        for dev,commit_date in self.backend.get_parsed_commit():
            if dev not in self.values:
                self.commits[dev] = 0
                self.values[dev] = []
                self.dates[dev] = []
            self.commits[dev] += 1
            if commit_date in self.dates[dev]:
                self.values[dev][
                            self.dates[dev].\
                            index(commit_date)] = self.commits[dev]
            else:
                self.dates[dev].append(commit_date)
                self.values[dev].append(self.commits[dev])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #color generator
        NUM_COLORS = len(self.dates)
        cm = get_cmap('gist_rainbow')
        cgen = (cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS))
        pls = []
        legends = []
        for name, data in self.values.items():
            pls.append(ax.plot_date(self.dates[name], data,
                       color=cgen.next()))
            legends.append(name)
        # Shink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height*0.8])


        fig.legend(pls, legends, 'upper left', ncol=5)
        savefig(output_filename)
