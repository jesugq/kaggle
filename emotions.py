# Imports
import csv
import time
import requests

# Settings
url = "https://apiv2.indico.io/sentiment"
key = "5bf59ad3450f583a8505fd13e44e8606"
settings = "&data="

# Opening Files
targetname = "./emotions.csv"
readername = "./kaggle/Training.csv"
targetfile = open(targetname, "w+")
readerfile = open(readername, encoding="ISO-8859-1")

# Table header creation
csvtarget = csv.writer(targetfile)
csvtarget.writerow(["emotion", "text", "score"])

# Obtain Text
csvreader = csv.reader(readerfile, delimiter=',')
next(csvreader)
csvtarget = csv.writer(targetfile)
for row in csvreader:
    text = row[0]
    score = row[1]
    payload = "".join((settings, text))
    
    # Request to JSON
    response = requests.request("POST", url, headers={"X-ApiKey": key}, data={"data": payload.encode('utf-8')})
    data = response.json()
    print(data)

# Closing Files
targetfile.close()
readerfile.close()