# Imports
import time
import requests
import shared

# Define HTTP Protocols
site        = "indicoio"
analysis    = "sentimenthq"
url, headers, arguments = shared.defineProtocol(site, analysis)

# Define file paths
type        = "testing"
result      = "sentimenthq"
readerpath, writerpath = shared.getPaths(type, result)

# Define file objects
writetype   = "w+"
readerfile, writerfile = shared.openFiles(readerpath, writerpath, writetype)

# Define csv objects
readercsv, writercsv = shared.createBuilders(readerfile, writerfile)
if (writetype == "w+"):|
    titles = [
        "index",
        "rating",
        "sentiment",
    ]
    shared.createTitles(writercsv, titles)

# Iteration calls
index = 1
target = 0
for row in readercsv:
    # Iteration Management
    if index <= target:
        printf("Advancing: " + str(index))
        index += 1
        continue
    else:
        print(index)

    # Get the values from the reader
    instance, review, rating = shared.getItems(type, row)
    review = shared.parseReview(review)

    # Unique to IndicoIO, add text to the data argument
    arguments["data"] = review
    payload = arguments

    # Call an HTTP fetch request
    response, json = shared.fetchAnalysis(url, headers, payload)
    if response.status_code != 200:
        print("Line " + str(index) + " was not retrieved properly.")
        json = "0.5"
    else:
        json = json["results"];
    
    # Get the values formatted
    values = [
        index,
        rating,
        json,
    ]

    # Create a row per values array
    shared.createRow(writercsv, values)

    # Predict IndicoIO's rate limit
    if index%250 == 0:
        time.sleep(3)
    index += 1

# Close Files
shared.closeFiles(readerfile, writerfile)