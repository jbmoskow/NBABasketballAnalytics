# The-Process-Revisted
## Bayesian analysis of NBA draft picks

### Collecting the data
Running the *Scraper.py* scripts (which use *beautifulsoup*) I obtained data from basketballreference.com for a large selection of NBA seasons, including a list of draft picks, Top 10 in VORP (Value over replacement player), and a list of all active players for each season. I then converted the data to a pandas DataFrame and saved to a csv file

### Bayesian analysis
By looking ahead at future seasons, I was able to determine the probability of a Top 5 draft pick ending up as Top 10  in VORP (this is our posterior probability or *P(A|B)*). This is a conditional probability that can be solved for using [Bayes Rule](https://en.wikipedia.org/wiki/Bayes%27_theorem).

<img src="https://latex.codecogs.com/svg.latex?\Large&space;P(A|B)=\frac{P(B|A)P(A)}{P(B)}"/>

where *P(A)* is our prior, the probability that a randomly selected NBA player is a Top 10 player
where *P(B)* is the probability of a randomly selected NBA player being a Top 5 draft pick.
where *P(B|A)* is our likelihood, what is the probability of a Top 10 player being a Top 5 draft pick.
