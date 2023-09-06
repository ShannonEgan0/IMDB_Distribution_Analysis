install.packages("tidyverse")
install.packages("ggplot2")

library(tidyverse)
library(ggplot2)
library(plotly)

# Specifying filters for original dataset
vote_number <- 1039
start_year <- 1960


imdb <- read.delim("IMDB Data/title_basics.tsv")

imdb_vote_count <- read.delim("IMDB Data/title_ratings.tsv")

# Need to verify this all, rearranged for efficiency, assuming merge will
# inner join as expected

# Plots the full distribution of ALL films average ratings
# Hovers predictably at 7.5
ggplot(data = imdb_vote_count) +
  geom_bar(mapping=aes(x=averageRating), fill="#f5c518")

summarize(imdb_vote_count, mean(numVotes), n())

# Filtering the data by number of votes
vote_filter <- imdb_vote_count %>% 
  filter(numVotes >= vote_number)

# Filtering to just films, min year and non-adult
imdb_filtered <- imdb %>% 
  filter(titleType == 'movie' & startYear >= start_year & isAdult == 0)

# Attempting to join both data imports to have ratings alongside details
imdb_merged <- merge(imdb_filtered, vote_filter, by="tconst")
summarize(imdb_merged, mean(numVotes), n())

# Plotting distribution of all films (post filter)
ggplot(data = imdb_merged) +
  geom_bar(mapping=aes(x=averageRating), fill="#f5c518")

# Removing redundant columns from data set
imdb_reduced <- select(imdb_merged, -isAdult, 
                       -endYear, -averageRating, -titleType)

# Writing file output for use with python dist compiling tool
write.csv(i, "movie_titles.csv", fileEncoding = "UTF-8", row.names = FALSE)
