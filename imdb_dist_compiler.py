import pandas as pd
import imdb_dist_scrape
import csv

data = pd.read_csv("C:\\Code\\R\\movie_titles.csv", encoding='utf8')
titles = data['tconst']
movie_data = []

completed = list(pd.read_csv("film_hists.csv", encoding='utf8')['tconst'])

print(f"{len(titles) - len(completed)} / {len(titles)} films remaining for scraping")

with open("film_hists.csv", 'a') as outfile:
    writer = csv.writer(outfile)
    for i in titles:
        if i not in completed:
            film_title, weighted_rating, mean_rating, h = imdb_dist_scrape.imdb_histogram(i)
            if mean_rating:
                hists = [h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10]]
                info = [i, weighted_rating, mean_rating] + hists
                movie_data.append(info)
                writer.writerow(info)
                print(f"{i} - {film_title}")
            else:
                print(f"No rating data for {i} - {film_title} found, may not have been released")

movie_data = pd.read_csv("film_hists.csv", encoding='utf8')
combo = data.merge(movie_data, on='tconst', how="inner")
combo.to_csv("test.csv")
