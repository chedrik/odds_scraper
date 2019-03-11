from datetime import datetime
import numpy as np
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import HoverTool, LinearColorMapper, ColorBar, PrintfTickFormatter, BasicTicker
from bokeh.transform import transform
import bokeh.palettes

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
                month = game['update_time'].month + 1 if month_wrap_idx and idx >= month_wrap_idx else game['update_time'].month
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
                    'prices': items[:, 1]
                })
    return source


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

    # this is the colormap from the original NYTimes plot
    # colors = bokeh.palettes.Viridis256[40]
    # nominal_mapper = LinearColorMapper(palette="Viridis256", low=-140, high=-100)
    # #nominal_mapper = LinearColorMapper(palette=colors, low=-200, high=200)

    tools = "pan"

    # fetch data from db as column source
    home_spread_source = convert_odds_to_source(game, 'home_spread')
    away_spread_source = convert_odds_to_source(game, 'away_spread')
    home_ml_source = convert_odds_to_source(game, 'home_ml')
    away_ml_source = convert_odds_to_source(game, 'away_ml')
    over_source = convert_odds_to_source(game, 'over')
    under_source = convert_odds_to_source(game, 'under')

    # gen figures and add tools
    spread = figure(tools=tools, plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    ml = figure(tools=tools,  plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    over = figure(tools=tools, plot_width=700, plot_height=300, x_axis_type="datetime", toolbar_location=None)
    # color_bar = ColorBar(color_mapper=nominal_mapper, location=(0, 0),
    #                      ticker=BasicTicker(desired_num_ticks=len(colors)),
    #                      formatter=PrintfTickFormatter(format="%d%%"))
    #
    # spread.add_layout(color_bar, 'right')
    spread.add_tools(hover_tool)
    ml.add_tools(hover_tool_ml)
    over.add_tools(hover_tool)

    # scatter plots
    # spread.scatter('date', 'odds', source=home_spread_source, fill_color=transform('prices', nominal_mapper))
    spread.scatter('date', 'odds', source=home_spread_source)
    spread.scatter('date', 'odds', source=away_spread_source)
    ml.scatter('date', 'prices', source=home_ml_source)
    ml.scatter('date', 'prices', source=away_ml_source)
    over.scatter('date', 'odds', source=over_source)
    over.scatter('date', 'odds', source=under_source)

    # set up each figure as as tab for easy viz
    spread_tab = Panel(child=spread, title="spread")
    ml_tab = Panel(child=ml, title="moneylines")
    over_tab = Panel(child=over, title="over/under")
    return Tabs(tabs=[spread_tab, ml_tab, over_tab])
