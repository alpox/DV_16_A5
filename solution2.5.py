import numpy as np
import plotly
from plotly import tools
import plotly.graph_objs as go
import movies as mv

movies = mv.get_all_movie_data()

years = []

genre_agg = {}

total = {}

for title, movie in movies.iteritems():
    if not 'genre' in movie or not 'year' in movie:
        continue
    
    year = movie['year']
    genres = movie['genre']

    if year == None: continue

    if year < 1915 or year > 2013:
        continue
    
    if not year in years:
        years.append(year)

    for genre in genres:
        if not genre in genre_agg:
            genre_agg[genre] = {}

        if not year in genre_agg[genre]:
            genre_agg[genre][year] = 1
        else:
            genre_agg[genre][year] += 1
        
        if not year in total:
            total[year] = 1
        else:
            total[year] += 1

years = sorted(years)

data = []

colors = ["#0a72ff", "#1eff06", "#ff1902", "#2dfefe", "#827c01", "#fe07a6", "#a8879f", "#fcff04", "#c602fe", "#16be61", "#ff9569", "#05b3ff", "#ecffa7", "#3f8670", "#e992ff", "#ffb209", "#e72955", "#83bf02", "#bba67b", "#fe7eb1", "#7570c1", "#85bfd1", "#f97505", "#9f52e9", "#8ffec2", "#dad045", "#b85f60", "#fe4df2", "#75ff6c", "#78a55a", "#ae6a02", "#bebeff", "#ffb3b3", "#a4fe04", "#ffc876", "#c548a7", "#d6492b", "#547da7", "#358b06", "#95caa9", "#07b990", "#feb6e9", "#c9ff76", "#02b708", "#7b7a6e", "#1090fb", "#a46d41", "#09ffa9", "#bb76b7", "#06b5b6", "#df307c", "#9b83fd", "#ff757c", "#0cd9fd", "#bdba61", "#c89d26", "#91df7e", "#108c49", "#7b7d40", "#fdd801", "#048699", "#fc9d40", "#ff0f3b", "#87a72c", "#a25cc2", "#b95a82", "#bb8a80", "#cce733", "#f7b58d", "#adaaab", "#c141c8", "#08fbd8", "#ff6de4", "#c26040", "#bb9bf6", "#b08f44", "#6d96de", "#8dcaff", "#5be51c", "#68c948", "#ff5fb8", "#7f9872", "#9aa5ca", "#bad292", "#c32fe4", "#fc92df", "#e08eaa", "#fd0afd", "#2daad4", "#d96d2a", "#69e0c9", "#ce4b69", "#79ca8d", "#6e8e9a", "#ffec83", "#de0fb5", "#8471a2", "#bbd766", "#e94805", "#06ff54", "#9cf046", "#6a63ff", "#05e774", "#e38c7b", "#f6ff75", "#3cda96", "#d68e4b", "#d774fe", "#feca4c", "#80ff95", "#5571e1", "#6da9a1", "#a5a20d", "#d5484a", "#688326", "#e7d08f", "#4e8653", "#5cad4c", "#c19bcf", "#ff0e76", "#d3ff0b", "#a66877", "#6ddde3", "#a544fe", "#c2fdb5", "#8f7955", "#fd735b", "#8497fd", "#fd919d", "#fdf346", "#fe5581", "#fd4e50", "#0ca82e", "#d4a8b2", "#d14e91", "#0d9069", "#0c8bca", "#fd9403", "#d5b401", "#adc32e", "#efacfe", "#9da668", "#57b093", "#787791", "#ff6f39", "#9e790a", "#d18903", "#abb49a", "#a06790", "#cf70cb", "#c8fe96", "#488834", "#dcbf55", "#e82f23", "#9a90d5", "#9cd54d", "#c7936c", "#05dc4a", "#98f372", "#907275", "#167dcf", "#db2b9f", "#16b16e", "#49a802", "#66cd1d", "#905fdc", "#cecd02", "#a376ca", "#939540", "#a7e103", "#d9ac6e", "#099334", "#db7701", "#3facbd", "#a0cb76", "#6aa3d5", "#dcaf98", "#b6692e", "#a76a59", "#04908e", "#d771ab", "#a69683", "#8268d0", "#72ab79", "#f70c8b", "#ebaa4c", "#9ce7b8", "#5f837a", "#df708c", "#ad9c32", "#39ffc2", "#d28388", "#79d5f9", "#e35eff", "#ffaf72", "#55e0b3", "#e8c0fe", "#6a69ed", "#fe07d3", "#0c86af"]


cumulative = [0 for y in years]

q = -1

for genre, values in genre_agg.iteritems():
    q += 1

    ydata = []
    for year in years:
        if year in values:
            ydata.append(float(values[year]) / float(total[year]) * 100)
        else:
            ydata.append(0)

    cumulative = [(ydata[i] or 0) + cumulative[i] for i in range(len(ydata))]

    p = go.Scatter(
        x=years, 
        y=cumulative, 
        name=genre,
        text=[str(y) for y in ydata],
        hoverinfo='text+name',
        fill='tonexty',
        marker=dict(
            color=colors[q]
        ),
        mode='lines')
    data.append(p)

layout = go.Layout(
    showlegend=True,
    yaxis=dict(
        ticksuffix="%"
    )
)

plotly.plotly.plot({'data': data, 'layout': layout})