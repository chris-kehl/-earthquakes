## install rtweet from CRAN
## install dev version of rtweet from github
devtools::install_github("mkearney/rtweet")

# Install the following packages
install.packages(c("ROAuth", "plyr, stringr", "ggplot2","wordcloud"),dependencies=T)

## load the package libraries
library(rtweet)
library(ROAuth)
library(plyr)
library(stringr)
library(ggplot2)
library(wordcloud)
library(tm)
library(SnowballC)

## install devtools package if it's not already
if (!requireNamespace("devtools", quietly = TRUE)) 
  install.packages("devtools")

## access token method: create token and save it as an environment variable
create_token(
  app = "chris_kehl",
  consumer_key = "dvkGkS6njgX53nx2ejztmqkJA",
  consumer_secret = "av6ZVYgrJk8dHPyWKw5DHfcOS9VhXyjfT2sKr4I19A6V5l2sAh",
  access_token = "1250247235-sEAAMIHF069nldOEAs3oY7CqV8eCEpvt8aCZ79m",
  access_secret = "J4erlmUGawTlGGRNKrjiXf9d2O6ZifSjwiAECRp8o7R5x")

## search for 18000 tweets using the rstats hashtag
eq.list <- search_tweets(
  "#earthquake", n = 18000, include_rts = FALSE
)
eq.df = twListToDF(MLB.List)
earthquake <- write.table(eq.list$text, file="~/Documents/data_files/earthquakes/earthquake.txt",  row.names = F, quote = F, sep="\t")

# Create a Corpus
eqCorpus <- Corpus(VectorSource(eq.list$text))

# Convert to Plain Text document
eqCorpus <- tm_map(eqCorpus, PlainTextDocument)

# Remove all punctuation, stopwords
eqCorpus <- tm_map(eqCorpus, removeWords, stopwords('english'))

# set up stemming
eqCorpus <- tm_map(eqCorpus, stemDocument)

# wordcloud
wordcloud(eqCorpus, max.words = 100)

## plot time series of tweets
ts_plot(eq.list, "3 hours") +
  ggplot2::theme_minimal() +
  ggplot2::theme(plot.title = ggplot2::element_text(face = "bold")) +
  ggplot2::labs(
    x = NULL, y = NULL,
    title = "Frequency of #earthquakes Twitter statuses from past 9 days",
    subtitle = "Twitter status (tweet) counts aggregated using three-hour intervals",
    caption = "\nSource: Data collected from Twitter's REST API via rtweet"
  )

## create lat/lng variables using all available tweet and profile geo-location data
eq <- lat_lng(eq.list)

## plot state boundaries
par(mar = c(0, 0, 0, 0))
maps::map("world", lwd = .90)


## plot lat and lng points onto state map
with(eq, points(lng, lat, pch = 20, cex = .75, col = rgb(0, .3, .7, .75)))

