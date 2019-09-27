import requests
import plotly.plotly as py
import plotly.graph_objs as go
from bs4 import BeautifulSoup as soup

# This program uses BeautifulSoup to scrape foxsports for soccer stats and export
# to 3 csv files - Goals, Assists, Saves.
# Display leaders and ranks in graphs on plotly.
# Author: Leticia Garcia-Sainz

page_link = "https://www.foxsports.com/soccer/stats?competition=2"

# fetch content from url
page_response = requests.get(page_link, timeout=5)

# parse html
page_content = soup(page_response.content, "html.parser")

# grab containers - goals, assists, saves
containers = page_content.findAll("div", {"class":"wisbb_leaders"})
container = containers[0]

# create csv files
filename1 = "wisbb_goals.csv"
filename2 = "wisbb_assists.csv"
filename3 = "wisbb_saves.csv"

f1 = open(filename1, "w")
f2 = open(filename2, "w")
f3 = open(filename3, "w")

headers = "rank, player, value\n"

f1.write(headers)
f2.write(headers)
f3.write(headers)

name_list = []
value_list = []

# method to find player info within container and write to csv
def findPlayer(filename):
    player_container = container.findAll("tr")
    p = player_container[0]
    for p in player_container:
        rank = p.find("span", {"class":"wisbb_leaderRank"})
        name = p.find("span", {"class":"wisbb_leaderName"})
        value = p.find("span", {"class":"wisbb_leaderValue"})

        filename.write(rank.text + "," + name.text + "," + value.text + "\n")

        # append names and values to list for plotly graph creation
        name_list.append(name.text)
        value_list.append(value.text)

    # create plotly bar graph (created on their website)
    data = [go.Bar(
                x = name_list,
                y = value_list
    )]
    py.plot(data, filename=title_container.text)
    # clear list for next function call
    del name_list[:]
    del value_list[:]
    filename.close()

# loop through the "leaders" containers
for container in containers:

    title_container = container.find("span", {"class":"wisbb_leaderTitle"})

    # find container for goals
    if (title_container.text == "Goals"):
        findPlayer(f1)

    # find container for assists
    elif (title_container.text == "Assists"):
        findPlayer(f2)

    #  find container for Saves
    elif (title_container.text == "Saves"):
        findPlayer(f3)
