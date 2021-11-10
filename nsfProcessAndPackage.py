from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET
from os import listdir
import pickle

DataYD = dict()

directory = "awards"
for f in listdir(directory):
    try:
        root = ET.parse('awards/%s'%f).getroot()
        title = root.find("Award").findtext('AwardTitle')
        id = root.find("Award").findtext('AwardID')
        abstract = root.find("Award").findtext('AbstractNarration')
        year = root.find("Award").find("Investigator").findtext('StartDate')[-4:]
        amount = float(root.find("Award").findtext("AwardAmount"))     
        words = word_tokenize(abstract)
        titlewords = word_tokenize(title)
        division = root.find("Award").find("Organization").find("Directorate").findtext("Abbreviation")
        fname = root.find("Award").find("Investigator").findtext('FirstName')
        thisdata = dict()
        if division == "" or division == None:
            division = "NON"
        division = ''.join([x if x.isalpha() else '' for x in division])
        thisdata['amount'] = amount
        thisdata['words'] = words
        thisdata['titlewords'] = titlewords
        thisdata['fname'] = fname
        if year not in DataYD:
            DataYD[year] = dict()
        if division not in DataYD[year]:
            DataYD[year][division] = dict()
        DataYD[year][division][id] = thisdata
    except:
        pass
        print("Passed!")

for y in DataYD:
    for d in DataYD[y]:
       file = open("pickled-data/" + str(d) + "-" + str(y) + ".dat", "wb")
       pickle.dump(DataYD[y][d], file)
       file.close()