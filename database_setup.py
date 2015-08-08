## Not used in current version


import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(200), nullable=False)
    address = Column(String(200))
    postal_code = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    phone_number = Column(String(12))

    inspections = relationship("Inspections",  backref="restaurant")
    violations = relationship("Violations",  backref="restaurant")
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'         : self.id,
           'address'        : self.address,
           'postal_code'        : self.postal_code,
           'latitude'       : self.latitude,
           'longitude'      : self.longitude,
           'phone_number'       : self.phone_number           
       }
 
class Inspections(Base):
    __tablename__ = 'inspections'

    business_id =Column(Integer,ForeignKey('restaurant.id'))
    id = Column(Integer, primary_key = True)
    date = Column(String(20), nullable=False)
    score = Column(Integer)
    insp_type = Column(String(200))
    

    @property
    def serialize(self):
       
       return {
           'id'         : self.business_id,
           'date'         : self.date,
           'score'         : self.score,
           'type'       : self.insp_type
       }

class Violations(Base):
    __tablename__ = 'inspections'

    business_id =Column(Integer,ForeignKey('restaurant.id'))
    id = Column(Integer, primary_key = True)
    date = Column(String(20), nullable = False)
    typeID = Column(Integer, nullable = False)
    risk_category = Column(String(20), nullable = False)
    description = Column(String(200), nullable = False)
    

    @property
    def serialize(self):  
       return {
           'id'         : self.business_id,
           'date'         : self.date,
           'type'         : self.typeID,
           'risk_category'       : self.risk_category,
           'description'       : self.description
       }
 

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
