from app import db, models
from app.views import preprocess
from datetime import datetime
import csv
import string

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


rep = {}

with open("./data/businesses_plus.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for data in reader:
        i += 1
        if i == 1:
            continue
        if data[0] in rep:
            #print rep[data[0]], data
            continue
        rep[data[0]] = i
        rec = models.Restaurant(id = int(data[0]),
                         name = preprocess(data[1]),
                         address = preprocess(data[2]),
                         postal_code = int(data[4]) if data[4].isdigit() else None,
                         latitude = float(data[5]) if isFloat(data[5]) else None,
                         longitude = float(data[6]) if isFloat(data[6]) else None,
                         phone_number = data[7][1:4]+'-'+data[7][4:7]+'-'+data[7][7:11] if data[7].isdigit() else None)
        db.session.add(rec)
        if i % 1000 == 0:
            db.session.flush()
    db.session.commit()


with open("./data/inspections_plus.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for data in reader:
        i += 1
        if i == 1:
            continue
        rec = models.Inspections(business_id = int(data[0]),
                                date = datetime.strptime(data[2], '%Y%m%d') if data[2] != '' else None,
                                score = int(data[1]) if data[1].isdigit() else None,
                                insp_type = data[3])      
        db.session.add(rec)
        if i % 1000 == 0:
            db.session.flush()
    db.session.commit()

with open("./data/violations_plus.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for data in reader:
        i += 1
        if i == 1:
            continue
        rec = models.Violations(business_id = int(data[0]),
                                date = datetime.strptime(data[1], '%Y%m%d') if data[1] != '' else None,
                                typeID = int(data[2]) if data[2].isdigit() else -1,
                                risk_category = data[3],
                                description = data[4])
        db.session.add(rec)
        if i % 1000 == 0:
            db.session.flush()
    db.session.commit()



    
