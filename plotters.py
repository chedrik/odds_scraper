from datetime import datetime
import numpy as np
from bokeh.plotting import figure


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


def make_plot(game):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    times, items = convert_odds_to_list(game, 'over')  # TODO: iterate for each object, set up overlay / menu to rotate
    p = figure(tools=TOOLS, plot_width=300, plot_height=300, x_axis_type="datetime")
    p.scatter(times, items[:,0], size=12, color="black", alpha=0.5)

    return p
