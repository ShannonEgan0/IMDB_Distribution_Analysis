from bs4 import BeautifulSoup
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys


def main():
    title = sys.argv[1]
    if not re.match(r"tt[0-9]{4,}", title):
        data = pd.read_csv("movie_titles.csv", encoding='utf8')
        title2 = data[data.values == title]['tconst'].values
        if len(title2):
            title = title2[0]
        else:
            print(f"Title or title id: '{title}' not found")
            return 0
    imdb_histogram(title, verbose=True, plot=True)


def imdb_histogram(title_id, verbose=False, plot=False):
    url = "https://www.imdb.com/title/" + title_id + "/ratings"
    html_text = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    soup = BeautifulSoup(html_text.content, features="html.parser")

    json_data = soup.find(id="__NEXT_DATA__").text
    json_data = json.loads(json_data)

    try:
        film_title = json_data["props"]["pageProps"]["contentData"]["entityMetadata"]["titleText"]["text"]
    except KeyError():
        print(f"{title_id} may not exist or has not been released, skipping to next film")
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

    if verbose:
        print(f"\nIMDB Rating Breakdown for {title_id} - {film_title}")
        print("Weighted Rating :", weighted_rating)
        print("Mean Rating :", mean_rating)
        for i in histograms:
            print(i["rating"], ":", i["voteCount"])

    if plot:
        fig, ax = plt.subplots()
        plt.xlabel("Number of Votes")
        max_votes = max(histograms_out.values())
        plt.xlim(0, max_votes + max_votes * 0.1)
        plt.ylabel("Vote Score")
        plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        bars = plt.barh(list(histograms_out.keys()), histograms_out.values(), color="#f5c518")
        ax.bar_label(bars, padding=10)
        plt.show()

    return film_title, weighted_rating, mean_rating, histograms_out


if __name__ == '__main__':
    main()
