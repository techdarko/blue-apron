# BlueApron Recipe Scraper - Recipe Filename Grabber

# link, filename, Recipe Title, Recipe title 2, description, servings, calories, cooking time low, cooking time high, is beef, is poultry, is pork, is lamb, is fish, is shellfish, is vegetarian


# import BeautifulSoup4, urllib2, os, csv
from bs4 import BeautifulSoup
import requests
import os
import re
import csv
import sys

site_prefix="https://www.blueapron.com/"
image_prefix="/Users/dgilmartin/recipes/images/"
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
    if i == 2:
        break
    # Grab webpage for recipe
    soup = BeautifulSoup(requests.get("https://www.blueapron.com/" + link).text, "html.parser")
    href = soup.find_all("a", class_="pdf-download-link")
    temp = href[0]["href"].decode('unicode_escape''ignore').encode('utf-8','ignore')
    name = temp[temp.rindex('/')+1:]
    main_title = soup.find_all("h1", class_="main-title")[0].contents[0].decode('unicode_escape','ignore').encode('utf-8','ignore')
    sub_title = soup.find_all("h2", class_="sub-title")[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    description = soup.find_all(itemprop='description')[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    servings = soup.find_all(itemprop='servings')[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    calories = soup.find_all(itemprop='calories')[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    mincooktime = soup.find_all(itemprop='calories')[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    maxcooktime = soup.find_all(itemprop='calories')[0].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    recipe_image= soup.find_all(class_='rec-splash-img')[0]["src"].contents[0].decode('unicode_escape''ignore').encode('utf-8','ignore')
    r = requests.get("https:"+recipe_image)
    with open(image_prefix+name[:-4]+'.jpg', "wb") as jpg:
        jpg.write(r.content)
    print(name)
    print(main_title)
    print(sub_title)
    print(servings)
    print(calories)
    print(mincooktime)
    print(maxcooktime)
    print(recipe_image)



href = soup.find_all("a", class_="pdf-download-link")
    temp = soup.find_all("a", class_="pdf-download-link")[0]["href"].decode('unicode_escape').encode('utf-8','ignore')
    name = temp[temp.rindex('/')+1:]