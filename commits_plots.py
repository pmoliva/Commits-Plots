import numpy.numarray as na
from pylab import *
import datetime
import re
import subprocess
import abc

class BaseBackend(object):
    __metaclass__=abc.ABCMeta


    @abc.abstractmethod
    def create_tmp_file(self):
        return


    @abc.abstractmethod
    def get_parsed_commit(self):
        return

class SVNBackend(BaseBackend):
    """
    svn log |grep [0-9] | trac
    """
    TEMP_FILENALE = 'svn_log_tmp.txt'
    DIR = '/tmp'
    def create_tmp_file(self):
        subprocess.\
            Popen("svn log | grep [0-9] | trac | awk '{print $3,$5}' > %s/%s'"\
                % (self.DIR, self. TEMP_FILENAME), shell=True)


    def get_parsed_commit(self):
        """
        file format: 'dev  %Y-%m-%d'
        """
        f = open('%s/%s' % (self.DIR, self.TEMP_FILE), 'r')
        for line in f:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(re.sub(r'\n',
                                                      '', info[2]), 
                                                      '%Y-%m-%d'))
        f.close()


class GitBackend(BaseBackend):
    """
    git log | egrep 'Author|Date' | sed '$!N;s/\n/ /
    """
    TEMP_FILENAME = 'svn_log_tmp.txt'
    DIR = '/tmp'
    def create_tmp_file(self):

        "git log | egrep 'Author|Date' | sed '$!N;s/\n/ /' | awk '{print $2,$6,$7,$9}'"
        subprocess.\
            Popen("git log | egrep 'Author|Date'" 
                    "| sed '$!N;s/\\n/ /' | "
                    "tac |"
                    "awk '{print $2,$6,$7,$9}' > %s/%s"
                    % (self.DIR, self.TEMP_FILENAME), 
                    shell=True)

    def get_parsed_commit(self):
        f = open('%s/%s' % (self.DIR, self.TEMP_FILENAME), 'r')
        for line in f:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(
                re.sub('\n', '', ' '.join(info[1:])), '%b %d %Y'))
        f.close()

        

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


    def plot_chart(self, output_filename):
        self.backend.create_tmp_file()
        for dev, date in self.backend.get_parsed_commit():
            if dev in self.devs:
                self.devs[dev] += 1;
            else:
                self.devs[dev] = 1
        for label, point in self.devs.items():
            self.labels.append(label)
            self.data.append(point)
        xlocations = na.array(range(len(self.data)))+0.5
        width = 0.5
        bar(xlocations, self.data, width=width)
        max_bar = max(self.data)
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


    def plot_chart(self, output_filename):
        self.backend.create_tmp_file()
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
        fig.legend(pls, legends, 'upper right', ncol=5)
        savefig(output_filename)


if __name__ == '__main__':
    backend = GitBackend()

    cbar = CommitsBarChart(backend)
    cbar.plot_chart('bar_chart')
    tchart = CommitsTimeSeries(backend)
    tchart.plot_chart('time_series')
