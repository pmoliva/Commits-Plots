import numpy.numarray as na

from pylab import *
import datetime
import re
import subprocess

class SVNBackend:
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
        file = open('%s/%s' % (self.DIR, self.TEMP_FILE), 'r')
        for line in file:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(re.sub(r'\n',
                                                      '', info[2]), 
                                                      '%Y-%m-%d'))
        file.close()


class GitBackend:
    """
    git log | egrep 'Author|Date' | sed '$!N;s/\n/ /
    """
    TEMP_FILENALE = 'svn_log_tmp.txt'
    DIR = '/tmp'
    def create_tmp_file(self):

        "git log | egrep 'Author|Date' | sed '$!N;s/\n/ /' | awk '{print $2,$6,$7,$9}'"
        subprocess.\
            Popen("git log | egrep 'Author|Date' | sed '$!N;s/\n/ /' | awk '{print $2,$6,$7,$9}'> %s/%s"\
                % (self.DIR, self. TEMP_FILENAME), shell=True)

    def get_parsed_commit(self):
        file = open('%s/%s' % (self.DIR, self.TEMP_FILE), 'r')
        for line in file:
            info = line.split(' ')
            yield (info[0], datetime.datetime.strptime(''.join(info[1:]), 
                                                      '%b %d %Y'))
        file.close()

        

class CommitsChart():
    src_filename = None
    

    def plot_chart(self, output_filename):
        pass


class CommitsBarChart(CommitsChart):
    labels = []
    data =   []
    devs = {}


    def  __init__(self, file_name):
        self.src_filename = file_name


    def plot_chart(self, output_filename):
        src = open(self.src_filename, 'r')
        for line in src:
            info = line.split(' ')
            if info[0] in self.devs:
                self.devs[info[0]] += 1;
            else:
                self.devs[info[0]] = 1
        for label, point in self.devs.items():
            self.labels.append(label)
            self.data.append(point)
        src.close()
        xlocations = na.array(range(len(self.data)))+0.5
        width = 0.5
        bar(xlocations, self.data, width=width)
        yticks(range(0, 350, 50))
        xticks(xlocations+ width/2, self.labels)
        xlim(0, xlocations[-1]+width*2)
        title("Number of commits")
        gca().get_xaxis().tick_bottom()
        gca().get_yaxis().tick_left()
        savefig(output_filename)


class CommitsTimeSeries(CommitsChart):
    dates = {}
    values = {}
    commits = {}
    def __init__(self, filename):
        self.src_filename = filename


    def plot_chart(self, output_filename):
        src = open(self.src_filename, 'r')
        for line in src:
            info = line.split(' ')
            if info[0] not in self.values:
                self.commits[info[0]] = 0
                self.values[info[0]] = []
                self.dates[info[0]] = []
            self.commits[info[0]] += 1
            commit_date =  datetime.datetime.strptime(re.sub(r'\n',
                                                      '', info[2]), 
                                                      '%Y-%m-%d')
            if commit_date in self.dates[info[0]]:
                self.values[info[0]][
                            self.dates[info[0]].\
                            index(commit_date)] = self.commits[info[0]]
            else:
                self.dates[info[0]].append(commit_date)
                self.values[info[0]].append(self.commits[info[0]])
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
    cbar = CommitsBarChart('log_teams.txt')
    cbar.plot_chart('bar_chart')
    tchart = CommitsTimeSeries('log_teams.txt')
    tchart.plot_chart('time_series')
