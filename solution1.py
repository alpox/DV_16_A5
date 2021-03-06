import numpy as np
import plotly
from plotly import tools
import plotly.graph_objs as go
import movies as mv

movies = mv.get_all_movie_data()

aggs = {}
nums = {}

for title, mov in movies.iteritems():
    if 'country' not in mov or mov['country'] != 'Switzerland': continue

    year = mov['year']
    if not year: continue

    idx = year%2000
    if year >= 2000 and year <= 2010 \
            and 'rating' in mov and 'genre' in mov:
        genres = mov['genre']

        for genre in genres:
            if genre in aggs:
                aggs[genre][idx] = aggs[genre][idx] + mov['rating']
                nums[genre][idx] = nums[genre][idx] + 1
            else:
                aggs[genre] = np.zeros(11)
                aggs[genre][idx] = mov['rating']
                nums[genre] = np.zeros(11)
                nums[genre][idx] = 1

data = []
rows = []
years = np.arange(2000, 2011).tolist()
it = 0
colors = ["#0a72ff", "#1eff06", "#ff1902", "#2dfefe", "#827c01", "#fe07a6", "#a8879f", "#fcff04", "#c602fe", "#16be61", "#ff9569", "#05b3ff", "#ecffa7", "#3f8670", "#e992ff", "#ffb209", "#e72955", "#83bf02", "#bba67b", "#fe7eb1", "#7570c1", "#85bfd1", "#f97505", "#9f52e9", "#8ffec2", "#dad045", "#b85f60", "#fe4df2", "#75ff6c", "#78a55a", "#ae6a02", "#bebeff", "#ffb3b3", "#a4fe04", "#ffc876", "#c548a7", "#d6492b", "#547da7", "#358b06", "#95caa9", "#07b990", "#feb6e9", "#c9ff76", "#02b708", "#7b7a6e", "#1090fb", "#a46d41", "#09ffa9", "#bb76b7", "#06b5b6", "#df307c", "#9b83fd", "#ff757c", "#0cd9fd", "#bdba61", "#c89d26", "#91df7e", "#108c49", "#7b7d40", "#fdd801", "#048699", "#fc9d40", "#ff0f3b", "#87a72c", "#a25cc2", "#b95a82", "#bb8a80", "#cce733", "#f7b58d", "#adaaab", "#c141c8", "#08fbd8", "#ff6de4", "#c26040", "#bb9bf6", "#b08f44", "#6d96de", "#8dcaff", "#5be51c", "#68c948", "#ff5fb8", "#7f9872", "#9aa5ca", "#bad292", "#c32fe4", "#fc92df", "#e08eaa", "#fd0afd", "#2daad4", "#d96d2a", "#69e0c9", "#ce4b69", "#79ca8d", "#6e8e9a", "#ffec83", "#de0fb5", "#8471a2", "#bbd766", "#e94805", "#06ff54", "#9cf046", "#6a63ff", "#05e774", "#e38c7b", "#f6ff75", "#3cda96", "#d68e4b", "#d774fe", "#feca4c", "#80ff95", "#5571e1", "#6da9a1", "#a5a20d", "#d5484a", "#688326", "#e7d08f", "#4e8653", "#5cad4c", "#c19bcf", "#ff0e76", "#d3ff0b", "#a66877", "#6ddde3", "#a544fe", "#c2fdb5", "#8f7955", "#fd735b", "#8497fd", "#fd919d", "#fdf346", "#fe5581", "#fd4e50", "#0ca82e", "#d4a8b2", "#d14e91", "#0d9069", "#0c8bca", "#fd9403", "#d5b401", "#adc32e", "#efacfe", "#9da668", "#57b093", "#787791", "#ff6f39", "#9e790a", "#d18903", "#abb49a", "#a06790", "#cf70cb", "#c8fe96", "#488834", "#dcbf55", "#e82f23", "#9a90d5", "#9cd54d", "#c7936c", "#05dc4a", "#98f372", "#907275", "#167dcf", "#db2b9f", "#16b16e", "#49a802", "#66cd1d", "#905fdc", "#cecd02", "#a376ca", "#939540", "#a7e103", "#d9ac6e", "#099334", "#db7701", "#3facbd", "#a0cb76", "#6aa3d5", "#dcaf98", "#b6692e", "#a76a59", "#04908e", "#d771ab", "#a69683", "#8268d0", "#72ab79", "#f70c8b", "#ebaa4c", "#9ce7b8", "#5f837a", "#df708c", "#ad9c32", "#39ffc2", "#d28388", "#79d5f9", "#e35eff", "#ffaf72", "#55e0b3", "#e8c0fe", "#6a69ed", "#fe07d3", "#0c86af"]


means = np.zeros(11)
mnums = np.zeros(11)

for genre, agg in aggs.iteritems():
    for i in range(11):
        aggs[genre][i] = agg[i] / nums[genre][i]
        if not np.isnan(aggs[genre][i]):
            means[i] += aggs[genre][i]
            mnums[i] += 1
    
    it += 1
    trace = go.Scatter(
        x=years,
        y=aggs[genre],
        name=genre,
        mode='markers',
        marker={'color':colors[it-1]}
    )

    data.append(trace)

for i in range(len(means)):
    means[i] = means[i] / mnums[i]

data.append(go.Scatter(
    x=years,
    y=means,
    name='Mean',
    marker={'color': colors[21]}
))

layout = {
    'xaxis': {'title': 'Years'},
    'yaxis': {'title': 'Rating'},
    'title': 'Average yearly ratings of Swiss movies between 2000 and 2010 grouped by genre'
}

plotly.offline.plot({'data': data, 'layout': layout})
