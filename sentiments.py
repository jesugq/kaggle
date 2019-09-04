# Imports
import csv
import json
import time
import requests

# Settings
url = "https://api.meaningcloud.com/sentiment-2.1"
settings = "key=fa8df01f467649550a51ef4b9fd0221a&lang=en&txtf=plain&txt="
headers = {'content-type': 'application/x-www-form-urlencoded'}

# Opening Files
targetname = "./sentiments.csv"
readername = "./kaggle/Training.csv"
targetfile = open(targetname, "w+")
readerfile = open(readername, encoding="ISO-8859-1")

# Table header Creation
csvtarget = csv.writer(targetfile)
csvtarget.writerow(["model", "score_tag", "agreement", "subjectivity", "confidence", "irony", "text"])

# Obtain Text
csvreader = csv.reader(readerfile, delimiter=',')
next(csvreader)
csvtarget = csv.writer(targetfile)
for row in csvreader:
    text = row[0]
    payload = "".join((settings, text))

    # Request to JSON
    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
    data = response.json()

    # Get Attributes Individually
    model = data.get("model", "")
    score_tag = data.get("score_tag", "")
    agreement = data.get("agreement", "")
    subjectivity = data.get("subjectivity", "")
    confidence = data.get("confidence", "")
    irony = data.get("irony", "")

    # Write to CSV File
    csvtarget.writerow([model, score_tag, agreement, subjectivity, confidence, irony, text])
    
    # MeaningCloud's Requests per Second Limit
    time.sleep(2)
# Closing Files
targetfile.close()
readerfile.close()