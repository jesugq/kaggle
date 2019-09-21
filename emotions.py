#####                               Settings                               #####
# Imports
import csv
import json
import time
import requests
import urllib.parse

# Defining Protocol
def defineProtocol():
    url = "https://apiv2.indico.io/emotion"
    headers = {'X-ApiKey': '5bf59ad3450f583a8505fd13e44e8606'}

    return url, headers

# Defining Arguments
def defineArguments():
    arguments = {
        "data": ''
    }

    return arguments

# Opening Files
def openFiles():
    readername = "../input/Training.csv"
    writername = "../extracted/emotions.csv"
    readerfile = open(readername, encoding="ISO-8859-1")
    writerfile = open(writername, "a+")
    
    return readerfile, writerfile

# Closing Files
def closeFiles(readerfile, writerfile):
    readerfile.close()
    writerfile.close()

# Creating CSV Builders
def createBuilders(readerfile, writerfile):
    readercsv = csv.reader(readerfile, delimiter=',')
    writercsv = csv.writer(writerfile)
    
    # Ignore readerfile's header
    next(readercsv)
    return readercsv, writercsv

# Scroll to position specified when Indico crashes
def scrollToPosition(index, position, readercsv):
    while index < position:
        index += 1
        next(readercsv)

    return index

# Obtain position, text and rating
def obtainValues(row):
    text = row[0]
    rating = row[1]

    return text, rating

# Call the Meaning Cloud API and return answer
def httpEmotions(url, headers, payload):
    response = requests.request("POST", url, data=payload, headers=headers)
    json = response.json()
    json = json["results"]

    return response, json

def mockJason():
    json = {
        "results": {
            "anger": 0.5,
            "joy": 0.5,
            "fear": 0.5,
            "sadness": 0.5,
            "surprise": 0.5
        }
    }

    return json

# Create the header of the csv result file
def createHeader(writercsv):
    writercsv.writerow(
        [
            "index",
            "rating",
            "anger",
            "joy",
            "fear",
            "sadness",
            "surprise",
        ]
    )

# Create each row of the csv result file
def createRow(writercsv, index, rating, data):
    writercsv.writerow(
        [
            index,
            rating,
            data["anger"],
            data["joy"],
            data["fear"],
            data["sadness"],
            data["surprise"],
        ]
    )

# Call each attribute individually
def extractAttributes(json):
    data = dict()

    data["anger"] = json['anger']
    data["joy"] = json['joy']
    data["fear"] = json['fear']
    data["sadness"] = json['sadness']
    data["surprise"] = json['surprise']

    return data

#####                                Logic                                #####
# Get settings
url, headers = defineProtocol()
arguments = defineArguments()

# Get files and builders
readerfile, writerfile = openFiles()
readercsv, writercsv = createBuilders(readerfile, writerfile)

# Write the header
# createHeader(writercsv)

# Or scroll the reader down if continuing a crashed instance
index = 1
position = 1122
index = scrollToPosition(index, position, readercsv)
print("Starting at index ", index, " in this run.")

# Run for every line in the readerfile
for row in readercsv:
    # Obtain the values from each row
    text, rating = obtainValues(row)

    # Parse for usage in http request
    parsed = urllib.parse.quote(text)
    arguments["data"] = parsed
    payload = arguments

    # Call http request with error handler
    response, json = httpEmotions(url, headers, payload)
    if response.status_code != 200:
        json = mockJason()
        print("Line ", index, " was not retrieved properly.")
    data = extractAttributes(json)

    # Write the obtained value
    createRow(writercsv, index, rating, data)

    # Predict IndicoIO's rate limit
    if index%250 == 0:
        time.sleep(5)
    index += 1

    
# Close files
closeFiles(readerfile, writerfile)