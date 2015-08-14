from app import db, models


def main():
    restaurants = models.Restaurant.query.all()
    i = 1
    for r in restaurants:
        print r.id, r.name
        db.session.delete(r)
        if i%1000 == 0:
        	db.session.flush()
        i += 1
    db.session.commit()


    restaurants = models.Inspections.query.all()
    i = 0
    for r in restaurants:
        print r.business_id, r.date
        db.session.delete(r)
        if i%1000 == 0:
        	db.session.flush()
        i += 1
    db.session.commit()

    restaurants = models.Violations.query.all()
    i = 0
    for r in restaurants:
        print r.business_id, r.date, r.description
        db.session.delete(r)
        if i%1000 == 0:
        	db.session.flush()
        i += 1
    db.session.commit()


if __name__ == '__main__':
    main()