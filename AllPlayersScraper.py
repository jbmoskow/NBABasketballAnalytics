from bs4 import BeautifulSoup
import certifi
import urllib3
import pandas

seasons = [i for i in range(1981, 2017)]  # Just look at (1980-1981 to 2015-2016 seasons) range(1981,2017)

# Iterate through NBA y from 1980-2015 and grab top 5 draft picks
for year in seasons:

    player_data = []  # init matrix

    url = "http://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()) # check for SSL verification
    response = http.request('GET', url)  # grab html data

    soup = BeautifulSoup(response.data, "lxml")  # convert to soup object
    column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]  # grab column headers

    data_rows = soup.findAll('tr')[1:]  # grab all player data for this NBA season

    for i in range(len(data_rows)):

        player_row = []

        for td in data_rows[i].findAll('td'):  # for each stats column
            player_row.append(td.getText())

        player_data.append(player_row)

    df = pandas.DataFrame(player_data, columns=column_headers[1:])
    filename = "AllPlayerData_" + str(year) + '.csv'
    df.to_csv(filename)

