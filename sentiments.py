#####                               Settings                               #####
# Imports
import csv
import json
import time
import requests
import urllib.parse

# Defining Protocol
def defineProtocol():
    url = "https://api.meaningcloud.com/sentiment-2.1"
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    return url, headers

# Defining Arguments
def defineArguments():
    key = "key=fa8df01f467649550a51ef4b9fd0221a"
    lang = "lang=en"
    txtf = "plain"
    uw = "uw=y"
    txt = "txt="
    args = key +"&"+ lang +"&"+ txtf +"&"+ uw +"&"+ txt

    return args

# Opening Files
def openFiles():
    readername = "../input/Training.csv"
    writername = "../extracted/sentiments.csv"
    readerfile = open(readername, encoding="ISO-8859-1")
    writerfile = open(writername, "w+")
    
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

# Obtain position, text and rating
def obtainValues(row):
    text = row[0]
    rating = row[1]

    return text, rating

# Call the Meaning Cloud API and return answer
def httpSentiments(url, headers, payload):
    response = requests.request("POST", url, data=payload, headers=headers)
    json = response.json()

    return response, json

# Create the header of the csv result file
def createHeader(writercsv):
    writercsv.writerow(
        [
            "index",
            "rating",
            "model",
            "score_tag",
            "agreement",
            "subjectivity",
            "confidence",
            "irony",
        ]
    )

# Create each row of the csv result file
def createRow(writercsv, index, rating, data):
    writercsv.writerow(
        [
            index,
            rating,
            data["model"],
            data["score_tag"],
            data["agreement"],
            data["subjectivity"],
            data["confidence"],
            data["irony"],
        ]
    )

# Call each attribute individually
def extractAttributes(json):
    data = dict()

    data["model"] = json['model']
    data["score_tag"] = json["score_tag"]
    data["agreement"] = json["agreement"]
    data["subjectivity"] = json["subjectivity"]
    data["confidence"] = json["confidence"]
    data["irony"] = json["irony"]

    return data

#####                                Logic                                #####
# Get settings
url, headers = defineProtocol()
arguments = defineArguments()

# Get files and builders
readerfile, writerfile = openFiles()
readercsv, writercsv = createBuilders(readerfile, writerfile)

# Write the header
createHeader(writercsv)

# Run for every line in the readerfile
index = 1
for row in readercsv:
    # Obtain the values from each row
    text, rating = obtainValues(row)

    # Parse for usage in http request
    parsed = urllib.parse.quote(text)
    payload = arguments + parsed

    # Call http request
    response, json = httpSentiments(url, headers, payload)
    data = extractAttributes(json)

    # Write the obtained value
    createRow(writercsv, index, rating, data)

    # Respect MeaningCloud's rate limit
    index += 1
    time.sleep(0.6)
    
# Close files
closeFiles(readerfile, writerfile)