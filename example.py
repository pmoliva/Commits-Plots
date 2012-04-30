from commits_plots import  CommitsTimeSeries, CommitsBarChart
from backend import SVNBackend


if __name__ == '__main__':
    backend = SVNBackend()

    cbar = CommitsBarChart(backend)
    cbar.plot_chart('/home/pedro/interpretes/desarrollo/web/', 'bar_chart')
    tchart = CommitsTimeSeries(backend)
    tchart.plot_chart('/home/pedro/interpretes/desarrollo/web/', 'time_series')
