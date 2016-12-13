import numpy as np
import plotly
from plotly import tools
import plotly.graph_objs as go
import movies as mv
import cufflinks as cf
import pandas as pd
from pandas import DataFrame as df

movies = mv.get_all_movie_data()

years = []

genre_agg = {}

for title, movie in movies.iteritems():
    if not 'genre' in movie or not 'year' in movie:
        continue
    
    year = movie['year']
    genres = movie['genre']

    if year == None: continue

    if not year in years:
        years.append(year)

    for genre in genres:
        if not genre in genre_agg:
            genre_agg[genre] = {}

        if not year in genre_agg[genre]:
            genre_agg[genre][year] = 1
        else:
            genre_agg[genre][year] += 1

years = sorted(years)

data = []
for genre, values in genre_agg.iteritems():
    ydata = []
    for year in years:
        if year in values:
            ydata.append(values[year])
        else:
            ydata.append(None)

    p = go.Scatter(x=years, y=ydata, name=genre, fill='tonexty', mode='lines')
    data.append(p)

layout = go.Layout(
    showlegend=True
)

plotly.offline.plot({'data': data, 'layout': layout})

'''
groups = movies.groupby(['year', 'genre'])

df = groups['title'].count().unstack(level=-1).dropna(how='all').head(-1)

df2 = df.divide(df.T.sum(), axis=0)
txt = (df2 * 100).applymap(lambda x: '%.2f' % x + '%')

figure = df2.iplot(kind='area', asFigure=True, fill='tonexty')
plotly.offline.plot(figure)

'''