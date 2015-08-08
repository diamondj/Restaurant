from hashlib import md5
from app import db, manager
from flask import jsonify
import json

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
   
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256))
    postal_code = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone_number = db.Column(db.String(16))

    inspections = db.relationship("Inspections",  backref=db.backref('restaurant', uselist = True, lazy='dynamic'))
    violations = db.relationship("Violations",  backref=db.backref('restaurant', uselist = True, lazy='dynamic'))
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name' : self.name,
           'id' : self.id,
           'address' : self.address,
           'postal_code' : self.postal_code,
           'latitude' : self.latitude,
           'longitude' : self.longitude,
           'phone_number' : self.phone_number,           
       }
 
class Inspections(db.Model):
    __tablename__ = 'inspections'

    business_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer)
    insp_type = db.Column(db.String(128))
    

    @property
    def serialize(self):
       
       return {
           'id'         : self.business_id,
           'date'         : self.date,
           'score'         : self.score,
           'type'       : self.insp_type,
       }

    def __repo__(self):

      return str(self.business_id) + " " + self.insp_type

class Violations(db.Model):
    __tablename__ = 'violations'

    business_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    typeID = db.Column(db.Integer, nullable = False)
    risk_category = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    

    @property
    def serialize(self):  
       return {
           'id'         : self.business_id,
           'date'         : self.date,
           'type'         : self.typeID,
           'risk_category'       : self.risk_category,
           'description'       : self.description,
       }

if __name__ == '__main__':
    manager.run()
