from datetime import datetime
import numpy as np
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components

import json

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers
def convert_odds_to_list(game, item):  # TODO: better name for this
    item_list = []
    item_times_list = []
    dict_items = game[item]

    days = dict_items.keys()
    days.sort()
    days = map(int, days)
    # month wrapping to get proper order TODO: year wrapping?!?!?!?!
    day_diff = np.array([t - s for s, t in zip(days, days[1:])])
    month_wrap_idx = np.where(day_diff > 1)
    if month_wrap_idx[0]:
        days = days[month_wrap_idx[0][0] + 1:] + days[:month_wrap_idx[0][0] + 1]

    for idx, day in enumerate(days):
        hours = game[item][str(day)].keys()
        hours.sort()
        for hour in hours:
            minutes = game[item][str(day)][hour]
            for minute_data in minutes:
                item_list.append(minute_data[1])

                month = game['update_time'].month + 1 if month_wrap_idx and idx >= month_wrap_idx else game['update_time'].month
                time = datetime(game['update_time'].year, month, day, int(hour), int(minute_data[0]))
                item_times_list.append(time)

    return np.array(item_times_list), np.array(item_list)


colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

def make_plot(games):

    # create some data
    # x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]
    # x2 = [2, 5, 7, 15, 18, 19, 25, 28, 9, 10, 4]
    # y2 = [2, 4, 6, 9, 15, 18, 0, 8, 2, 25, 28]
    # x3 = [0, 1, 0, 8, 2, 4, 6, 9, 7, 8, 9]
    # y3 = [0, 8, 4, 6, 9, 15, 18, 19, 19, 25, 28]
    #
    # # select the tools we want
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    #
    # # the red and blue graphs will share this data range
    # xr1 = Range1d(start=0, end=30)
    # yr1 = Range1d(start=0, end=30)
    #
    # # only the green will use this data range
    # xr2 = Range1d(start=0, end=30)
    # yr2 = Range1d(start=0, end=30)
    #
    # # build our figures
    # p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
    # p1.scatter(x1, y1, size=12, color="red", alpha=0.5)
    #
    # p2 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
    # p2.scatter(x2, y2, size=12, color="blue", alpha=0.5)
    #
    # p3 = figure(x_range=xr2, y_range=yr2, tools=TOOLS, plot_width=300, plot_height=300)
    # p3.scatter(x3, y3, size=12, color="green", alpha=0.5)
    plots = []
    for game in games:
        times, items = convert_odds_to_list(game, 'over')
        p4 = figure(tools=TOOLS, plot_width=300, plot_height=300, x_axis_type="datetime")
        p4.scatter(times, items[:,0], size=12, color="black", alpha=0.5)
        plots.append(p4)
    # plots can be a single Bokeh Model, a list/tuple, or even a dictionary
    #plots = {'Red': p1, 'Blue': p2, 'Green': p3}
    #plots = (p1, p2, p3, p4)

    return tuple(plots)


