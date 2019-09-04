# Imports
import csv
import time
import requests

# Settings
url = "'X-ApiKey: 5bf59ad3450f583a8505fd13e44e8606' 'https://apiv2.indico.io/sentiment' --data '{\"data\": \""
lru = "\"}'"

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
    payload = url + text + lru
    print("\n\n")
    print(payload)
    print("\n\n")

    response = requests.request("GET", payload)
    data = response.json()

    csvtarget.writerow([response, text, score])

# Closing Files
targetfile.close()
readerfile.close()