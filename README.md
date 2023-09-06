# IMDB_Distribution_Analysis
Tools for investigating vote distributions in IMDB.

Can be used to easily isolate anomolous films that could be considered "controversial", or have a controversial response from voters. These tools expose things like purchased votes, racism, genocide denial, propaganda and political controversy.

IMDB currently offers datasets containing film details as well as mean scores, and the total number of votes submitted. Visibly available on the website however, but not quite as easily available, are the numbers of votes submitted for a film between (and inclusive of) 1 and 10. IMDB also nicely provide an interesting chart of these vote distributions (eg. LINK).
Given full knowledge of all films distributions, we can find an average, or expected distribution for a film at any score. (INSERT HOME ALONE OR HOOK OR SOMETHING HERE) Then, we can evaluate the deviation of a film's distribution from the expected one. The greater this deviation is, the more suspicious the film, and this often leads to interesting stories.

Provided in this repository is a python script to sequentially scrape and archive all film distributions from IMDB (from a curated list to reduce the time this would take), or just return the distribution of a particular film. Also included is an R script to calculate the expected distributions of sequential score brackets, parameterised with band width values (eg. width = 0.1, will return all bands of the form 6.9 - 7.1 etc.), then compare all films to their expected distributions using sum of squares regression.

TO BE UPDATED SOON

#### TO DO
- Add archived datetime to scraping tool
