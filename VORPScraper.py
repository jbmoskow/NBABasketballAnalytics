from bs4 import BeautifulSoup
import urllib3
import certifi
import pandas

player_data = []  # init matrix

url = "https://www.basketball-reference.com/leaders/vorp_top_10.html"

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())  # check for SSL verification
response = http.request('GET', url)  # grab html data

soup = BeautifulSoup(response.data, "lxml")  # convert to soup object
column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]  # grab column headers\

data_rows = soup.findAll('tr')[1:]  # grab all player data for this draft year

for i in range(38):  # just want the current season all the way to 1980-1981
    player_row = []

    for td in data_rows[i].findAll('td'):  # for each stats column
        player_row.append(td.getText())

    player_data.append(player_row)

df = pandas.DataFrame(player_data, columns=column_headers)
df.to_csv('VORPdata.csv')
