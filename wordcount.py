#####                               Settings                               #####
# Imports
import re
import csv
import urllib.parse

# Opening Files
def openFiles():
    readername = "../input/Testing.csv"
    writername = "../extracted/testing/wordcount.csv"
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
def obtainTrainingValues(row):
    text = row[0]
    rating = row[1]

    return text, rating
def obtainTestingValues(row):
    text = row[1]
    rating = "?"

    return text, rating

# Create the header of the csv result file
def createHeader(writercsv):
    writercsv.writerow(
        [
            "index",
            "rating",
            "wordcount"
        ]
    )

# Create each row of the csv result file
def createRow(writercsv, index, rating, wordcount):
    writercsv.writerow(
        [
            index,
            rating,
            wordcount
        ]
    )


#####                                Logic                                #####
# Get files and builders
readerfile, writerfile = openFiles()
readercsv, writercsv = createBuilders(readerfile, writerfile)

# Write the header
createHeader(writercsv)

# Run for every line in the readerfile
index = 1
for row in readercsv:
    # Obtain the values from each row
    text, rating = obtainTestingValues(row)

    # Parse for usage in word counter
    parsed = urllib.parse.quote(text)

    # Replace all weird characters %XX with a separator
    parsed = re.sub('%[0-9a-zA-Z][0-9a-zA-Z]|_', ',', parsed)

    # Split into words
    wordcount = 0
    words = parsed.split(',')
    for word in words:
        if word:
            wordcount += 1

    # Write the obtained value
    createRow(writercsv, index, rating, wordcount)

    # Keep track of the index
    index += 1
    
# Close files
closeFiles(readerfile, writerfile)