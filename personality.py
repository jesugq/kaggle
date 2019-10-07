# Import
import time
import shared
import requests

# Define http protocols.
site        = "indicoio"
analysis    = "personality"
url, headers, arguments = shared.defineProtocol(site, analysis)

# Define file paths.
type    = "testing"
result  = "personality"
readerpath, writerpath = shared.getPaths(type, result)

# Define file objects.
writetype = "w+"
readerfile, writerfile = shared.openFiles(readerpath, writerpath, writetype)

# Define csv objects.
readercsv, writercsv = shared.createBuilders(readerfile, writerfile)
if (writetype == "w+"):
    titles = [
        "index",
        "rating",
        "extraversion",
        "openness",
        "agreeableness",
        "conscientiousness",
    ]
    shared.createTitles(writercsv, titles)

# Iteration calls.
index = 1
target = 0
for row in readercsv:
    # Advance to where we left off
    if index <= target:
        print("Advancing: " + str(index))
        index += 1
        continue;
    else:
        print(index)

    # Get the values from the reader.
    instance, review, rating = shared.getItems(type, row)
    review = shared.parseReview(review)

    # Unique to IndicoIO, add text to the data argument
    arguments["data"] = review
    payload = arguments

    # Call an http fetch request
    response, json = shared.fetchAnalysis(url, headers, payload)
    if response.status_code != 200:
        print("Line " + str(index) + " was not retrieved properly")
        json = {
            'extraversion': "0.5",
            'openness': "0.5",
            'agreeableness': "0.5",
            'conscientiousness': "0.5",
        }
    else:
        json = json["results"]

    # Get the values formatted
    json["index"] = index
    json["rating"] = rating
    values = [
        json["index"],
        json["rating"],
        json["extraversion"],
        json["openness"],
        json["agreeableness"],
        json["conscientiousness"],
    ]

    # Create a row per values array
    shared.createRow(writercsv, values)

    # Predict IndicoIO's rate limit
    if index%250 == 0:
        time.sleep(5)
    index += 1

# Close files
shared.closeFiles(readerfile, writerfile)