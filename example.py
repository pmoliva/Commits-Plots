from commits_plots import  GitBackend, CommitsTimeSeries, CommitsBarChart


if __name__ == '__main__':
    backend = GitBackend()

    cbar = CommitsBarChart(backend)
    cbar.plot_chart('bar_chart')
    tchart = CommitsTimeSeries(backend)
    tchart.plot_chart('time_series')
