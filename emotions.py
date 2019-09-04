import indicoio
indicoio.config.api_key = '5bf59ad3450f583a8505fd13e44e8606'

# single example
first = indicoio.sentiment("I love writing code!")

# batch example
second = indicoio.sentiment([
    "I love writing code!",
    "Alexander and the Terrible, Horrible, No Good, Very Bad Day"
])

print(first)
print(second)