from bs4 import BeautifulSoup
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys


# Allows sctipt to be ran from terminal with argv[1] being the film title or code
def main():
    if len(sys.argv) > 0:
        title = sys.argv[1]
    else:
        print("No film specified.")
        print('Usage: "python imdb_dist_scrape.py film_title"')
        return 0
    if not re.match(r"^tt[0-9]{4,}", title):
        title = search_title(title)
    return imdb_histogram(title, verbose=True, plot=True)


# Function for looking up exact titles rather than title codes
# Requires pre-compiled list of film titles
def search_title(title):
    data = pd.read_csv("movie_titles.csv", encoding='utf8')
    title2 = data[data.values == title]['tconst'].values
    if len(title2):
        return title2[0]
    else:
        print(f"Title or title id: '{title}' not found")
        return 0


# Scrapes IMDB vote distribution from imdb.com based on input film title code
def imdb_histogram(title_id, verbose=False, plot=False):
    url = "https://www.imdb.com/title/" + title_id + "/ratings"
    html_text = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    soup = BeautifulSoup(html_text.content, features="html.parser")

    json_data = soup.find(id="__NEXT_DATA__").text
    json_data = json.loads(json_data)

    try:
        film_title = json_data["props"]["pageProps"]["contentData"]["entityMetadata"]["titleText"]["text"]
    except KeyError():
        print(f"{title_id} may not exist or has not been released")
        return 0, 0, 0, 0
    weighted_rating = json_data["props"]["pageProps"]["contentData"][
        "entityMetadata"]["ratingsSummary"]["aggregateRating"]
    histograms = json_data["props"]["pageProps"]["contentData"]["histogramData"]["histogramValues"]

    mean_rating = 0
    total_votes = 0
    histograms_out = dict()
    for i in histograms:
        mean_rating += int(i["rating"]) * int(i["voteCount"])
        total_votes += int(i["voteCount"])
        histograms_out.update({int(i["rating"]): int(i["voteCount"])})
    if total_votes:
        mean_rating = round(mean_rating / total_votes, 4)
    else:
        mean_rating = 0

    # If verbose set to True, this will print film details
    if verbose:
        print(f"\nIMDB Rating Breakdown for {title_id} - {film_title}")
        print("Weighted Rating :", weighted_rating)
        print("Mean Rating :", mean_rating)
        for i in histograms:
            print(i["rating"], ":", i["voteCount"])

    # If plot is set to True, a plot of the vote distribution will be displayed
    if plot:
        fig, ax = plt.subplots()
        plt.xlabel("Number of Votes")
        max_votes = max(histograms_out.values())
        lab_len = len(str(max_votes))
        plt.xlim(0, max_votes + max_votes * 0.03 * lab_len)
        plt.ylabel("Vote Score")
        plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        bars = plt.barh(list(histograms_out.keys()), histograms_out.values(), color="#f5c518")
        ax.bar_label(bars, padding=8)
        plt.show()

    return film_title, weighted_rating, mean_rating, histograms_out


if __name__ == '__main__':
    main()
