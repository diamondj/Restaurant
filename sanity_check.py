from app import db, models

restaurants = models.Restaurant.query.all()
i = 1
for r in restaurants:
    print r.id, r.name
    db.session.delete(r)
    if i%1000 == 0:
    	db.session.flush()
    i += 1
db.session.commit()
