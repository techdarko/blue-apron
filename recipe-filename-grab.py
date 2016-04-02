# BlueApron Recipe Scraper - Recipe Filename Grabber

# import BeautifulSoup4, urllib2, os, csv
from bs4 import BeautifulSoup
import requests
import os
import re
import csv
import sys

site_prefix="https://www.blueapron.com/"
save_location="/Users/dgilmartin/recipes/"

# Grab CSV of grabbed recipes and import into list for checking.
try:
    with open(save_location+'downloaded_recipes.csv', 'rb') as f:
        reader = csv.reader(f)
        grabbed = list(reader)
except:
    print("Cannot Import {0}downloaded_recipes.csv.\nPlease check the file and run the script again.\n".format(save_location))
    raw_input("Press Enter To Quit.")
    sys.exit("Import Error")
g = len(grabbed)
h = 0
while h < g:
    grabbed[h] = str(grabbed[h][0])
    h += 1

print("Imported {0} Previously Grabbed Recipes.\n".format(g))

# For each link in links, compare to imported CSV for previously grabbed recipes

i = 0
j = 0
file_names = []
for link in grabbed:
    if i == 10:
        break
    # Grab webpage for recipe
    soup = BeautifulSoup(requests.get("https://www.blueapron.com/" + link).text, "html.parser")
    href = soup.find_all("a", class_="pdf-download-link")
    temp = href[0]["href"].decode('unicode_escape').encode('ascii','ignore')
    name = temp[temp.rindex('/')+1:]
    print(name)
    file_names.append([link, name])
    j += 1
    i += 1
try:
    with open(save_location+'recipe_names1.csv', 'wb') as f:
        wr = csv.writer(f, lineterminator='\n')
        for val in file_names:
            wr.writerows([val])
except:
    print("Cannot Save Grabbed Recipes To {0}recipe_names.csv.\nPlease check the file and run the script again.\n".format(save_location))
    raw_input("Press Enter To Quit.")
    sys.exit("Import Error")


print("{0} Recipe Names Grabbed.\n".format(j))

print("{0} Total Recipes Grabbed.\n".format(len(grabbed)))

