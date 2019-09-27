import requests
from bs4 import BeautifulSoup as soup
import matplotlib
import matplotlib.pyplot as plt
import os

# This program uses BeautifulSoup to scrape foxsports for soccer stats and export
# to csv files - Goals, Assists.
# Display leaders and ranks in graphs with matplotlib.
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

f1 = open(filename1, "w")
f2 = open(filename2, "w")

headers = "rank, player, value\n"

f1.write(headers)
f2.write(headers)

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

    # create bar charts
    plt.bar(name_list, value_list)
    # plt.set_title(title_container.text)
    plt.xticks(rotation='82.5')
    plt.tight_layout()
    # save graph
    if not os.path.exists("images"):
        os.mkdir("images")
    plt.savefig(f'images/{title_container.text}')
    plt.close()

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
