import re
import os
import numpy as np
import pandas as pd

try:
   import cPickle as pickle
except:
   import pickle

pattern = '(.*?) +\((.*?)\)(?: +\(.*?\))?(?: +?\{(.*)\})?\t+?([\w\d?]+)$'
movieRegex = re.compile(pattern)

yearPattern = '(\d{4})'
yearRegex = re.compile(yearPattern)

def get_movies():
    movies = {}    

    with open('./data/movies.list', 'r') as file:
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
    with open('./data/countries.list', 'r') as file:
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

    with open('./data/ratings.list', 'r') as file:
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
    with open('./data/genres.list', 'r') as file:
        for line in file:
            m = movieRegex.match(line)

            if m == None: continue

            title = m.group(1)
            genre = m.group(4)

            if title in movies:
                if 'genre' in movies[title]:
                    movies[title]['genre'] += [genre]
                else:
                    movies[title]['genre'] = [genre]

    return movies

def get_all_movie_data():
    movies = {}

    if os.path.isfile("movies.bin"):
        with open('movies.bin', 'rb') as file:
            movies = pickle.load(file)
    else:
        movies = get_movies()
        movies = loadCountriesFor(movies)
        movies = loadRatingsFor(movies)
        movies = loadGenresFor(movies)
        with open('movies.bin', 'wb') as file:
            pickle.dump(movies, file, protocol=2)

    return movies

def movies_to_df(movies):
    return pd.DataFrame(movies.values(), index=movies.keys())