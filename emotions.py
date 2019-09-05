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
# for i in range(639):
next(csvreader)
csvtarget = csv.writer(targetfile)
index = 0
for row in csvreader:
    # Obtain values from our file
    index += 1
    text = row[0]
    score = row[1]
    
    # Request to JSON
    response = requests.request("POST", url, headers={"X-ApiKey": key}, data={"data": text.encode('utf-8')})
    data = response.json().get("results", "")

    # Get Attributes Individually
    try:
        anger = data.get("anger", "")
        joy = data.get("joy", "")
        fear = data.get("fear", "")
        sadness = data.get("sadness", "")
        surprise = data.get("surprise", "")
    except:
        print(data)
        print(response)

    # Write to CSV File
    csvtarget.writerow([anger, joy, fear, sadness, surprise, text, score])

    # Wait to prevent AttributeErrors due to going too fast
    if index > 500:
        time.sleep(2)
        index = 0

# Closing Files
targetfile.close()
readerfile.close()