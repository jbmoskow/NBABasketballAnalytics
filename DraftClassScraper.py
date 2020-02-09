from bs4 import BeautifulSoup
import certifi
import urllib3
import pandas

draft_years = [i for i in range(1980, 2016)]  # Just look at 1980-2015 draft classes
player_data = []  # init matrix

# Iterate through draft years from 1980-2015 and grab top 5 draft picks
for year in draft_years:

    url = "http://www.basketball-reference.com/draft/NBA_" + str(year) + ".html"

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()) # check for SSL verification
    response = http.request('GET', url)  # grab html data

    soup = BeautifulSoup(response.data, "lxml")  # convert to soup object
    column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]  # grab column headers
    column_headers.append("DraftYear")

    data_rows = soup.findAll('tr')[2:]  # grab all player data for this draft year

    for i in range(5):  # just select the 1st-5th draft picks, can be modified to get other picks
        player_row = []

        for td in data_rows[i].findAll('td'):  # for each stats column
            player_row.append(td.getText())

        player_row.append(str(year))  # add year
        player_data.append(player_row)

df = pandas.DataFrame(player_data, columns=column_headers[1:])
df.to_csv('DraftClassData.csv')

