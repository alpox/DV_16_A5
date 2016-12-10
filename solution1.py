import re
import os
import numpy as np
import matplotlib.pyplot as plt

try:
   import cPickle as pickle
except:
   import picklee

pattern = '(.*?) +\((.*?)\)(?: +\(.*?\))?(?: +?\{(.*)\})?\t+?([\w\d?]+)$'
movieRegex = re.compile(pattern)

yearPattern = '(\d{4})'
yearRegex = re.compile(yearPattern)

def get_movies():
    movies = {}    

    with open('../data/movies.list', 'r') as file:
        for line in file:
            m = movieRegex.match(line)

            if m == None: continue

            title = m.group(1)
            year = m.group(4)

            yearMatch = yearRegex.match(year)
            if not yearMatch:
                year = m.group(2)

                yearMatch2 = yearRegex.match(year)

                if not yearMatch2:
                    year = None
                else:
                    year = int(yearMatch2.group(1))
            else:
                year = int(yearMatch.group(1))

            movies[title] = { "title": title, "year": year }

    return movies

def loadCountriesFor(movies):
    with open('../data/countries.list', 'r') as file:
        for line in file:
            m = movieRegex.match(line)

            if m == None: continue

            title = m.group(1)
            country = m.group(4)

            if title in movies:
                movies[title]["country"] = country

    return movies

def loadRatingsFor(movies):
    isReading = False
    ratingsPattern = '[0-9.]{10} +?(\d+) +?([0-9.]+) +?([^ ].*?) +?\(.*?\)'
    ratingsRegex = re.compile(ratingsPattern)

    with open('../data/ratings.list', 'r') as file:
        for line in file:
            line = line.strip()
            if line == 'MOVIE RATINGS REPORT':
                isReading = True
            if not isReading: continue

            match = ratingsRegex.match(line)

            if not match: continue

            title = match.group(3)
            votes = match.group(1)
            rating = match.group(2)

            if title in movies:
                movies[title]['votes'] = int(votes)
                movies[title]['rating'] = float(rating)
    return movies

def loadGenresFor(movies):
    with open('../data/genres.list', 'r') as file:
        for line in file:
            m = movieRegex.match(line)

            if m == None: continue

            title = m.group(1)
            genre = m.group(4)

            if title in movies:
                movies[title]["genre"] = genre

    return movies

movies = {}

if os.path.isfile("movies.bin"):
    with open('movies.bin', 'rw') as file:
        movies = pickle.load(file)
else:
    movies = get_movies()
    movies = loadCountriesFor(movies)
    movies = loadRatingsFor(movies)
    movies = loadGenresFor(movies)
    with open('movies.bin', 'w') as file:
        pickle.dump(movies, file, protocol=2)

aggs = {}
nums = {}

for title, mov in movies.iteritems():
    if 'country' not in mov or mov['country'] != 'Switzerland': continue

    year = mov['year']
    if not year: continue

    idx = year%2000
    if year >= 2000 and year <= 2010 \
            and 'rating' in mov and 'genre' in mov:
        genre = mov['genre']

        if genre in aggs:
            aggs[genre][idx] = aggs[genre][idx] + mov['rating']
            nums[genre][idx] = nums[genre][idx] + 1
        else:
            aggs[genre] = np.zeros(11)
            aggs[genre][idx] = mov['rating']
            nums[genre] = np.zeros(11)
            nums[genre][idx] = 1

rows = []
years = np.arange(2000, 2011)

for genre, agg in aggs.iteritems():
    for i in range(11):
        aggs[genre][i] = agg[i] / nums[genre][i]
        
    rows.append(aggs[genre])

    
rows = np.row_stack(rows)
rows[np.isnan(rows)] = 0

plt.stackplot(years, rows)

plt.show()
