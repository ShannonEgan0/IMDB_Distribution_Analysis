# IMDB_Distribution_Analysis
Tools for investigating vote distributions in IMDB.

Can be used to easily isolate anomolous films that could be considered "controversial", or have a controversial response from voters. These tools expose things like purchased votes, racism, genocide denial, propaganda and political controversy.

IMDB currently offers datasets containing film details as well as mean scores, and the total number of votes submitted. Visibly available on the website however, but not quite as easily available, are the numbers of votes submitted for a film between (and inclusive of) 1 and 10. IMDB also nicely provide an interesting chart of these vote distributions (eg. [Alvin and the Chipmunks](https://www.imdb.com/title/tt0952640/ratings/?ref_=tt_ov_rt)). Given full knowledge of all films distributions, we can find an average, or expected distribution for a film at any score. Then, we can evaluate the deviation of a film's distribution from the expected one. The greater this deviation is, the more suspicious the film, and this often leads to interesting stories.

<p align="center">
  <img src="readme_files/Alvin and the Chipmunks.png" />
  <br>
  <i>Distribution comparison for votes for Alvin and the chimpunks (in yellow), compared to the expected distribution (in black)</i>
</p>

"Alvin and the Chimpunks (2007)", a family or child oriented film about three musical, anthropomorphic chipmunks, had an extremely predictable audience response based on films with average ratings of 5.51±0.2 (close to the average unweighted score of Alvin and the Chimpunks), with a calculated deviation based on a sum of squares difference of 4.6099e-05. It could be claimed that "Alvin and the Chimpunks" is unlikely to be a divisive or controversial film based on the audience response.

<p align="center">
  <img src="readme_files/The Promise.png" />
  <br>
  <i>Distribution comparison for votes for The Promise (in yellow), compared to the expected distribution (in black)</i>
</p>

In contrast to "Alvin and the Chimpunks", the film "The Promise (2016)", a film focused on the Armenian genocide, had a vote response far from the expected distribution, with a sum of squres difference of 0.3989. Voters for this film were heavily inclined to give this film either 1, or 10 stars, which does not follow typical voting patterns for a film with this average rating.

Provided in this repository is a python script to sequentially scrape and archive all film distributions from IMDB (from a curated list to reduce the time this would take), or just return the distribution of a particular film. Also included is an R script to calculate the expected distributions of sequential score brackets, parameterised with band width values (eg. width = 0.1, will return all bands of the form 6.9 - 7.1 etc.), then compare all films to their expected distributions using sum of squares regression.

TO BE UPDATED SOON

#### TO DO
- Add archived datetime to scraping tool
