install.packages("tidyverse")
install.packages("ggplot2")

library(tidyverse)
library(ggplot2)
library(plotly)


imdb <- read.delim("IMDB Data/title_basics.tsv")

imdb_vote_count <- read.delim("IMDB Data/title_ratings.tsv")

# Plots the full distribution of ALL films average ratings
# Hovers predictably at 7.5
ggplot(data = imdb_vote_count) +
  geom_bar(mapping=aes(x=averageRating), fill="#f5c518")

summarize(imdb_vote_count, mean(numVotes), n())

# Filtering the data by number of votes
filter_imdb <- imdb_vote_count %>% 
  filter(numVotes > 1038)
ggplot(data = filter_imdb) +
  geom_bar(mapping=aes(x=averageRating), fill="#f5c518")
summarize(filter_imdb, mean(numVotes), n())

# Attempting to join both data imports to have ratings alongside details
imdb_merged <- merge(imdb, filter_imdb, by="tconst")
summarize(imdb_merged, mean(numVotes), n())

# Filtering to just films, min year and non-adult
i <- imdb_merged %>% 
  filter(titleType == 'movie' & startYear >= 1960 & isAdult == 0)
summarize(i, mean(numVotes), n())
ggplot(data = i) +
  geom_bar(mapping=aes(x=averageRating), fill="#f5c518")


i <- select(i, -isAdult, -endYear, -averageRating, -titleType)

write.csv(i, "movie_titles.csv", fileEncoding = "UTF-8", row.names = FALSE)


# This is where the python script should be run to scrape in the dist data

# Reading the output distribution data merged with movie general data
imdb_dists <- select(read.csv("IMDB_distributions.csv"), -X)

cols = c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10")

for (i in cols) {
  imdb_dists[i] <- imdb_dists[i] / imdb_dists["numVotes"]
}


narrow_band <- function(data_table, value, band=0.2) {
  out <- data_table %>% 
    filter(mean_rating >= value - band, mean_rating <= value + band)
  return(out)
}


ur_dist <- function(data_table, plot=TRUE, rating=NULL) {
  a <- data_table %>% 
    summarize(mean(X1), mean(X2), mean(X3), mean(X4), mean(X5), mean(X6),
              mean(X7), mean(X8), mean(X9), mean(X10)) %>% 
    t()
  a <- data.frame(b=c(1,2,3,4,5,6,7,8,9,10), a)
  
  if (!is.null(rating)) {
    rating = paste("Rating:", rating)
  }
  
  if (plot == TRUE) {
    print(ggplot(data = a) +
      geom_col(mapping=aes(x=b, y=a), fill="#f5c518") +
      scale_x_continuous(breaks=seq(1, 10, 1)) + 
      labs(title = "IMDB Vote Distribution Comparison",
           x="Votes", y="% of votes at value",
           subtitle = rating))
  }
  return(a)
}


check_film <- function(title, data_table, band=0.2, plot=TRUE) {
  # Checking whether title is a code or a full name
  if (str_detect(title, regex("^tt[0-9]{4,}"))) {
    film <- filter(data_table, tconst == title)
    title <- film["primaryTitle"]
  } else {
    film <- filter(data_table, primaryTitle == title)
  }
  film <- t(film)
  
  mean_rating <- as.numeric(film[9])
  dist_ratings <- as.numeric(film[10:19])
  film_dist <- data.frame(b=c(1,2,3,4,5,6,7,8,9,10), dist_ratings)
  
  # Narrowing band
  data_table <- narrow_band(data_table, value=mean_rating, band=band)
  
  dist <- ur_dist(data_table, plot=FALSE)
  dist_size <- count(data_table)
  
  # Calculating the sum of squares of the film compared to expected distribution
  deviation <- sum((film_dist[2] - dist[2])**2)
  
  if (plot) {
    # Subtitle Text
    sub_text <- paste("Rating:", round(mean_rating, 3), 
                      "Sum Squared Deviation:", 
                      round(deviation, 3))
    
    # Add warning if dist size is low
    if (dist_size <= 1000) {
      sub_text <- paste(sub_text, "\n*** Warning: Distribution size is low:", 
                        dist_size,"  Consider increasing band size ***")
    }
    
    # Plotting comparison of ur distribution to the film distribution
    print(ggplot() +
      geom_col(data=dist, mapping=aes(x=b, y=100 * a), fill="#f5c518") +
      geom_line(data=film_dist, mapping=aes(x=b, y=100 * dist_ratings)) +
      geom_point(data=film_dist, mapping=aes(x=b, y=100 * dist_ratings)) +
      scale_x_continuous(breaks=seq(1, 10, 1)) + 
      labs(title = paste("IMDB Vote Distribution Comparison for", title),
           subtitle = sub_text, x="Votes", y="% of votes at value"))
  }
  return(deviation)
}


# Selecting film for comparison
title <- "tt2112096"

check_film(title, imdb_dists)


# This function finds all deviations for all films in the dataset
find_urs <- function(data_table) {
  print("Finding all diff values")
  to_add <- c()
  for (i in data_table[["tconst"]]) {
    diff <- check_film(i, data_table, plot=FALSE)
    to_add <- append(to_add, diff)
  }
  print("Finding diffs complete")
  data_table$deviation <- to_add
  return(data_table)
}


# Running function to create column of all deviations from the expected
# distributions for the entire dataset
imdb_dists <- find_urs(imdb_dists)

# Adding column to dataset comparing the weighted IMDB score to the unweighted
# score to find films IMDB has identified as suspicious
# Effectively introduces a "weighting" factor
imdb_dists$weight_unweight_ratio <- abs(c["weighted_rating"] - c["mean_rating"])

# Checking a series of progressive distributions to illustrate expected dists
checks <- 0:43 * 0.2 + 1.2
spaced_dists <- list()
for (i in checks) {
  new_dist <- narrow_band(imdb_dists, value = i)
  new_dist <- ur_dist(new_dist, rating = i)
  fig <- plot_ly(new_dist, x=~b, y=~a, type="bar")
  spaced_dists <- append(spaced_dists,
                         plot_ly(new_dist, x=~b, y=~a, type="bar")
                         )
}

new_dist <- narrow_band(imdb_dists, value = 6)
new_dist <- ur_dist(new_dist, plot=FALSE)

fig <- plot_ly(
  new_dist, x=~b, y=~a, type="bar"
)



fig <- fig %>% layout(title = "Basic Slider",
                      sliders = list(
                        list(
                          active = 1, 
                          currentvalue = list(prefix = "Color: "), 
                          steps = spaced_dists))) 

fig

