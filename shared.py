# Imports
import key
import re
import csv
import requests
import urllib.parse

# Returns paths used in reading and writing.
#   param type      Type to get, Training or Testing data.
#   param result    Filename of the result, e.g. Personality
#   return readerpath   Path to the reader file.
#   return writerpath   Path to the writer file.
def getPaths(type, result):
    if type == "training":
        readerpath = "../input/Training.csv"
        writerpath = "../extracted/training/" + result + ".csv"
        return readerpath, writerpath
    elif type == "testing":
        readerpath = "../input/Testing.csv"
        writerpath = "../extracted/testing/" + result + ".csv"
        return readerpath, writerpath
    else:
        raise Exception("The type was neither training or testing.")

# Opens two files
#   param readername    Filename of the file to read.
#   param writerprefix  Subpath of the file to write.
#   param writername    Filename of the file to write.
#   param writetype     Type to write, overwriting or appending.
#   return readerfile       Reader file.
#   return writherfile      Writer file.
def openFiles(readerpath, writerpath, writetype):
    readerfile = open(readerpath, encoding="ISO-8859-1")
    writerfile = open(writerpath, writetype)

    return readerfile, writerfile

# Closes two files.
#   param readerfile    Reader object to close.
#   param writerfile    Writer object to close.
def closeFiles(readerfile, writerfile):
    readerfile.close()
    writerfile.close()

# Create CSV builders.
#   param readerfile    File object to read.
#   param writerfile    File object to write.
#   return readercsv    CSV Object to read from.
#   return writercsv    CSV Object to write to.
def createBuilders(readerfile, writerfile):
    readercsv = csv.reader(readerfile, delimiter=",")
    writercsv = csv.writer(writerfile)
    next(readercsv)     # Ignores the header columns.

    return readercsv, writercsv

# Obtain values from the file.
#   param type      Type to get, Training or Testing data.
#   return index        ID of the Review.
#   return review       Review text.
#   return rating       Rating given by the reviewer.
def getItems(type, row):
    if type == "training":
        index = "?"
        review = row[0]
        rating = row[1]
        return index, review, rating
    elif type == "testing":
        index = row[0]
        review = row[1]
        rating = "?"
        return index, review, rating
    else:
        raise Exception("The type was neither training or testing.")

# Creates a title column.
#   param writercsv     Writer csv object to write to.
#   param titles        Array of values shown as titles.
def createTitles(writercsv, titles):
    writercsv.writerow(titles)

# Writes a row of values.
#   param writercsv     Writer csv object to write to.
#   param values        Array of values per title.
def createRow(writercsv, values):
    writercsv.writerow(values)

# Sanitizes the review.
#   param review        Review to sanitize.
#   return parsed       Sanitized review.
def parseReview(review):
    parsed = urllib.parse.quote(review)
    parsed = re.sub('%[0-9a-zA-Z][0-9a-zA-Z]|_', ',', parsed)
    return parsed

# Define http protocol
#   param site      Site to obtain the text analysis from.
#   param analysis  Type of analysis from said site.
def defineProtocol(site, analysis):
    if site == "meaningcloud":
        url = "https://api.meaningcloud.com/" + analysis
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        arguments = {
            "key": key.getAPIKey(),
            "lang": "en",
            "txtf": "plain",
            "uw": "y",
            "txt": "",
        }
        return url, headers, arguments
    elif site == "indicoio":
        url = "https://apiv2.indico.io/" + analysis
        headers = headers = {'X-ApiKey': key.getAPIKey()}
        arguments = {
            "data": "",
        }
        return url, headers, arguments
    else:
        raise Exception("The site was neither meaningcloud or indicoio.")

# Fetch the response from the text analysis site
#   param url       Url to fetch from.
#   param headers   Protocol headers.
#   param payload   Information to ask from the API.
def fetchAnalysis(url, headers, payload):
    response = requests.request("POST", url, data=payload, headers=headers)
    json = response.json()
    return response, json