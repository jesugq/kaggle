# Imports
import csv
import json
import time
import requests

# Settings
url = "https://apiv2.indico.io/emotion"
key = "5bf59ad3450f583a8505fd13e44e8606"

# Opening Files
targetname = "./emotions.csv"
readername = "./kaggle/Training.csv"
targetfile = open(targetname, "w+")
readerfile = open(readername, encoding="ISO-8859-1")

# Table header creation
csvtarget = csv.writer(targetfile)
csvtarget.writerow(["anger", "joy", "fear", "sadness", "surprise", "text", "score"])

# Obtain Text
csvreader = csv.reader(readerfile, delimiter=',')
next(csvreader)
csvtarget = csv.writer(targetfile)
for row in csvreader:
    # Obtain values from our file
    text = row[0]
    score = row[1]
    
    # Request to JSON
    response = requests.request("POST", url, headers={"X-ApiKey": key}, data={"data": text.encode('utf-8')})
    data = response.json().get("results", "")
    print(data)

    # Get Attributes Individually
    anger = data.get("anger", "")
    joy = data.get("joy", "")
    fear = data.get("fear", "")
    sadness = data.get("sadness", "")
    surprise = data.get("surprise", "")

    # Write to CSV File
    csvtarget.writerow([anger, joy, fear, sadness, surprise, text, score])

# Closing Files
targetfile.close()
readerfile.close()