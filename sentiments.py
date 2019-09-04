# Imports
import csv
import json
import requests

# Settings
url = "https://api.meaningcloud.com/sentiment-2.1"
settings = "key=fa8df01f467649550a51ef4b9fd0221a&lang=en&txtf=plain&txt="
headers = {'content-type': 'application/x-www-form-urlencoded'}

# Opening Files
targetname = "./sentiments.csv"
readername = "./kaggle/Training.csv"
targetfile = open(targetname, "a+")
readerfile = open(readername, encoding="ISO-8859-1")

# Table header Creation
opened = targetfile.read(1)
if not opened:
    csvtarget = csv.writer(targetfile)
    csvtarget.writerow(["model", "score_tag", "agreement", "subjectivity", "confidence", "irony"])

# Obtain Text
csvreader = csv.reader(readerfile, delimiter=',')
csvtarget = csv.writer(targetfile)
for row in csvreader:
    text = row[0]
    payload = "".join((settings, text))

    # Request to JSON
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
    data = response.json()

    # Write to CSV File
    csvtarget.writerow([data["model"], data["score_tag"], data["agreement"], data["subjectivity"], data["confidence"], data["irony"]])

# Closing Files
targetfile.close()
readerfile.close()