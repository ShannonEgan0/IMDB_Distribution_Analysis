import pandas as pd
import imdb_dist_scrape
import csv
from os import listdir
from datetime import datetime as dt

data = pd.read_csv("C:\\Code\\R\\movie_titles.csv", encoding='utf8')
titles = data['tconst']
movie_data = []

# Creating film_hists file if it doesn't already exist
if "film_hists.csv" not in listdir():
    open("film_hists.csv", 'w').close()
completed = list(pd.read_csv("film_hists.csv", encoding='utf8')['tconst'])

print(f"{len(titles) - len(completed)} / {len(titles)} films remaining for scraping")

with open("film_hists.csv", 'a') as outfile:
    writer = csv.writer(outfile)
    for i in titles:
        if i not in completed:
            film_title, weighted_rating, mean_rating, h = imdb_dist_scrape.imdb_histogram(i)
            scrape_time = dt.now()
            if mean_rating:
                hists = [h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10]]
                # Need to also append the date and time the data line was acquired below
                # Currently left unimplemented as the receiving R code has not been updated to handle it
                # Will amend with the next full scraping period
                info = [i, weighted_rating, mean_rating] + hists
                movie_data.append(info)
                writer.writerow(info)
                print(f"{i} - {film_title}")
            else:
                print(f"No rating data for {i} - {film_title} found, may not have been released")

# Combining distribution data with existing film data from IMDB
movie_data = pd.read_csv("film_hists.csv", encoding='utf8')
combo = data.merge(movie_data, on='tconst', how="inner")
combo.to_csv("IMDB_distributions.csv")
