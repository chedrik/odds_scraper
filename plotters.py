import numpy as np
from datetime import datetime
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import HoverTool, LinearColorMapper, ColorBar
from bokeh.models.tickers import FixedTicker
from bisect import bisect_left
from config import Config


def convert_odds_to_source(game, item):
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
                month = game['update_time'].month + 1 if month_wrap_idx and idx >= month_wrap_idx else game[
                    'update_time'].month
                time = datetime(game['update_time'].year, month, day, int(hour), int(minute_data[0]))
                item_times_list.append(time)
    times, items = np.array(item_times_list), np.array(item_list)
    if 'ml' in item:
        source = ColumnDataSource(data={
            'date': times,  # python datetime object as X axis
            'prices': items[:, ]
        })
    else:
        source = ColumnDataSource(data={
            'date': times,  # python datetime object as X axis
            'odds': items[:, 0],
            'prices': items[:, 1],
        })
    return source


def generate_color_bins(prices):
    # find max and min odds for favorite and dog to dynamically interpolate between set of colors
    neg_min, neg_max, pos_min, pos_max = -95., -100000., 100000., 105.
    for price in prices:
        if price < 0:
            if price < neg_min:
                neg_min = price
            if price > neg_max:
                neg_max = price
        else:
            if price > pos_max:
                pos_max = price
            if price < pos_min:
                pos_min = price

    neg_bins, pos_bins = None, None
    if neg_max != -100000.:  # has - numbers
        _, neg_bins = np.histogram([neg_min, neg_max], bins=7)
    if pos_min != 100000.:  # has + numbers
        _, pos_bins = np.histogram([pos_min, pos_max], bins=7)
        if pos_min != 100.:
            pos_bins = np.append(np.array(100.), pos_bins)
    if neg_bins is not None and pos_bins is not None:
        bins = np.concatenate((neg_bins, pos_bins))
        total_min = neg_min
        total_max = pos_max
    elif pos_bins is not None:
        bins = pos_bins
        total_min = pos_min
        total_max = pos_max
    else:
        bins = neg_bins
        total_min = neg_min
        total_max = neg_max

    return bins, total_min, total_max


def make_plot(game):
    # TODO: dynamic plot sizing once v 1.0.5 bokeh is released and scaled_width bug is fixed
    # define styling, tools, etc.
    hover_tool = HoverTool(
        tooltips=[
            ('time', '@date{%m-%d %H:%M}'),
            ('odds', '@odds{0.0 a}'),
            ('price', '@prices{0.0 a}')
        ],
        formatters={'date': 'datetime'},
        mode='vline'
    )
    hover_tool_ml = HoverTool(
        tooltips=[
            ('time', '@date{%m-%d %H:%M}'),
            ('price', '@prices{0.0 a}')
        ],
        formatters={'date': 'datetime'},
        mode='vline'
    )

    tools = "pan"

    # fetch data from db as column source
    home_spread_source = convert_odds_to_source(game, 'home_spread')
    away_spread_source = convert_odds_to_source(game, 'away_spread')
    home_ml_source = convert_odds_to_source(game, 'home_ml')
    away_ml_source = convert_odds_to_source(game, 'away_ml')
    over_source = convert_odds_to_source(game, 'over')
    under_source = convert_odds_to_source(game, 'under')

    # generate dynamic color scale and assign to spreads and totals (ml needs no color)
    colors = Config.COLORS
    spread_bins, sp_min, sp_max = generate_color_bins(np.concatenate((home_spread_source.data['prices'],
                                                                      away_spread_source.data['prices'])))
    over_bins, op_min, op_max = generate_color_bins(np.concatenate((over_source.data['prices'],
                                                                    under_source.data['prices'])))
    home_spread_source.data['color'] = [colors[min(max(bisect_left(spread_bins, price) - 1, 0), len(colors) - 1)]
                                        for price in home_spread_source.data['prices']]
    away_spread_source.data['color'] = [colors[min(max(bisect_left(spread_bins, price) - 1, 0), len(colors) - 1)]
                                        for price in away_spread_source.data['prices']]
    over_source.data['color'] = [colors[min(max(bisect_left(over_bins, price) - 1, 0), len(colors) - 1)]
                                 for price in over_source.data['prices']]
    under_source.data['color'] = [colors[min(max(bisect_left(over_bins, price) - 1, 0), len(colors) - 1)]
                                  for price in under_source.data['prices']]

    # gen color bar maps
    if sp_min < 0 < sp_max:
        spread_pal = colors
    elif sp_min < 0 and sp_max < 0:
        spread_pal = colors[:7]
    else:
        spread_pal = colors[8:]
    if op_min < 0 < op_max:
        over_pal = colors
    elif op_min < 0 and op_max < 0:
        over_pal = colors[:7]
    else:
        over_pal = colors[8:]
    spread_cmap = LinearColorMapper(palette=spread_pal, low=sp_min, high=sp_max)
    ou_cmap = LinearColorMapper(palette=over_pal, low=op_min, high=op_max)

    # gen figures and add tools, color bars
    spread = figure(tools=tools, plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    ml = figure(tools=tools, plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    over = figure(tools=tools, plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    spread.add_layout(ColorBar(color_mapper=spread_cmap, location=(0, 0),
                               ticker=FixedTicker(ticks=[sp_min, sp_max])), 'right')
    over.add_layout(ColorBar(color_mapper=ou_cmap, location=(0, 0),
                             ticker=FixedTicker(ticks=[op_min, op_max])), 'right')
    spread.add_tools(hover_tool)
    ml.add_tools(hover_tool_ml)
    over.add_tools(hover_tool)

    # make scatter plots
    spread.scatter(x='date', y='odds', source=home_spread_source, color='color', size=Config.MARKER_SIZE)
    spread.scatter(x='date', y='odds', source=away_spread_source, color='color', size=Config.MARKER_SIZE)
    ml.scatter(x='date', y='prices', source=home_ml_source, size=Config.MARKER_SIZE)
    ml.scatter(x='date', y='prices', source=away_ml_source, size=Config.MARKER_SIZE)
    over.scatter(x='date', y='odds', source=over_source, color='color', size=Config.MARKER_SIZE)
    over.scatter(x='date', y='odds', source=under_source, color='color', size=Config.MARKER_SIZE)

    # set up each figure as as tab for easy viz
    spread_tab = Panel(child=spread, title="spread")
    ml_tab = Panel(child=ml, title="moneylines")
    over_tab = Panel(child=over, title="over/under")

    return Tabs(tabs=[spread_tab, ml_tab, over_tab])
