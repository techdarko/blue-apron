# BlueApron Recipe Scraper - PDF Downloader

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

# Grab CSV of grabbed recipes and import into list for checking.
try:
    with open(save_location+'recipe_filenames.csv', 'rb') as f:
        reader = csv.reader(f)
        file_names = list(reader)
except:
    print("Cannot Import {0}downloaded_recipes.csv.\nPlease check the file and run the script again.\n".format(save_location))
    raw_input("Press Enter To Quit.")
    sys.exit("Import Error")


# Set Range For Cookbook Pages

i = range(1,100)

links = []

pages_done = 0

# For each page in range, call cookbook.js, parse, and make array of recipe addresses for grabbing pdfs.

for page in i:
    # Grab page
    soup = BeautifulSoup(requests.get("https://www.blueapron.com/cookbook.js?page={0}".format(page)).text, "html.parser")

    # Parse Page For a hrefs into list
    hrefs = soup.find_all('a', href=True)
    # Check list - If no hrefs found, break
    if len(hrefs) == 0:
        print("None Found On Page {0}".format(page))
        break
    # Iterate through list - grab href text and append to links list
    for a in hrefs:
        temp = (a["href"].decode('unicode_escape').encode('ascii','ignore'))
        links.append(re.sub('"','',temp))

    del links[-1]
    # For each page, announce completion and links grabbed (should be consistant across pages)
    print("Page {0}: Grabbed {1} Links.\n".format(page, len(links)))
    # Increment page counter
    pages_done += 1

# Announce total number of pages processed and total number of links grabbed
print("Pages Iterated. {0} Pages Processed, {1} Links Collected.\n".format(pages_done, len(links)))

# For each link in links, compare to imported CSV for previously grabbed recipes

j = 0
k = 0
l = 0
failed = []

for link in links:
    # Compare link to CSV, if found skip
    print link
    if any(gotten == link for gotten in grabbed):
        print("Skipping - Previously Grabbed")
        k += 1
        print("{0} of {1}\n".format((j+k+l),len(links)))
        continue

    # Grab webpage for recipe
    soup = BeautifulSoup(requests.get("https://www.blueapron.com/" + link).text, "html.parser")
    href = soup.find_all("a", class_="pdf-download-link")
    try:
        temp = href[0]["href"].decode('unicode_escape').encode('ascii','ignore')
    except:
        print("Cannot find link on {0}{1} - skipping.\n".format(site_prefix,link))
        failed.append((site_prefix+link))
        l += 1
        continue
    name = temp[temp.rindex('/')+1:]
    print(name)
    file_names.append([link, name])
    try:
        r = requests.get("https:"+temp)
        with open(save_location+name, "wb") as pdf:
            pdf.write(r.content)
        grabbed.append(link)
        j += 1
        print("{0} of {1}\n".format((j+k+l),len(links)))
    except (KeyboardInterrupt, SystemExit):
        with open(save_location+'downloaded_recipes.csv', 'wb') as f:
            wr = csv.writer(f, lineterminator='\n')
            for val in grabbed:
                wr.writerow([val])
    except:
        print("Cannot grab https:{0}".format(temp))
        l += 1
        print("{0} of {1}\n".format((j+k+l),len(links)))

try:
    with open(save_location+'downloaded_recipes.csv', 'wb') as f:
        wr = csv.writer(f, lineterminator='\n')
        for val in grabbed:
            wr.writerow([val])
except:
    print("Cannot Save Grabbed Recipes To {0}downloaded_recipes.csv.\nPlease check the file and run the script again.\n".format(save_location))
    raw_input("Press Enter To Quit.")
    sys.exit("Import Error")

try:
    with open(save_location+'recipe_names.csv', 'wb') as f:
        wr = csv.writer(f, lineterminator='\n')
        for val in file_names:
            wr.writerows(val)
except:
    print("Cannot Save Grabbed Recipes To {0}recipe_names.csv.\nPlease check the file and run the script again.\n".format(save_location))
    raw_input("Press Enter To Quit.")
    sys.exit("Import Error")


print("{0} New Recipes Grabbed.\n".format(j))
print("{0} Recipes Skipped.\n".format(k))
print("{0} Recipes Failed To Download.\n".format(l))
print("{0} Total Recipes Grabbed.\n".format(len(grabbed)))




