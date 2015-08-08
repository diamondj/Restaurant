from app import db, models
import csv
from datetime import datetime


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
