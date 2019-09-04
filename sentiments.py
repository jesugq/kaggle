# Imports
import csv
import json
import requests

# Settings
url = "https://api.meaningcloud.com/sentiment-2.1"
settings = "key=fa8df01f467649550a51ef4b9fd0221a&lang=en&txtf=plain&txt="
headers = {'content-type': 'application/x-www-form-urlencoded'}

# Text
text = "horrible customer service hotel stay february 3rd 4th 2007my friend picked hotel monaco appealing website online package included champagne late checkout 3 free valet gift spa weekend 	friend checked room hours earlier came later 	pulled valet young man just stood 	asked valet open said 	pull bags didn__�_�_ offer help 	got garment bag suitcase came car key room number says not valet 	car park car street pull 	left key working asked valet park car gets 	went room fine bottle champagne oil lotion gift spa 	dressed went came got bed noticed blood drops pillows sheets pillows 	disgusted just unbelievable 	called desk sent somebody 20 minutes later 	swapped sheets left apologizing 	sunday morning called desk speak management sheets aggravated rude 	apparently no manager kind supervisor weekend wait monday morning 	young man spoke said cover food adding person changed sheets said fresh blood rude tone 	checkout 3pm package booked 	12 1:30 staff maids tried walk room opening door apologizing closing 	people called saying check 12 remind package 	finally packed things went downstairs check 	quickly signed paper took 	way took closer look room 	unfortunately covered food offered charged valet 	called desk ask charges lady answered snapped saying aware problem experienced monday like told earlier 	life treated like hotel 	not sure hotel constantly problems lucky ones stay recommend anybody know 	 "
payload = "".join((settings, text))
print(payload)

# Request
response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)
print(response.json())

# Convert to JSON
data = response.json()

# File Emptyness Verifier
filename = "sentiments.csv"
file = open(filename)
opened = file.read(1)
file.close()

# Create Table Header
file = csv.writer(open(filename, "a+"))
if not opened:
    file.writerow(["model", "score_tag", "agreement", "subjectivity", "confidence", "irony"])
file.writerow([data["model"], data["score_tag"], data["agreement"], data["subjectivity"], data["confidence"], data["irony"]])