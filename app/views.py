from flask import render_template, flash, redirect, session, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from datetime import datetime
from app import app, db
from .forms import LoginForm, EditForm
from .models import Restaurant, Inspections, Violations
from sqlalchemy import desc, func, and_, or_
from sqlalchemy.orm import load_only

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import string
import json

def preprocess(s):
    s = s.strip()
    return string.capwords(s)


GoogleMaps(app)
SFgeo = (37.7833, -122.4167)


@app.route('/restaurant/<restaurant_id>/JSON', methods=['GET'])
def restaurantIDJSON(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    return jsonify(id = restaurant.serialize)

@app.route('/restaurant/name/<restaurant_name>/JSON', methods=['GET'])
def restaurantNameJSON(restaurant_name):
    restaurants = Restaurant.query.filter_by(name=preprocess(restaurant_name)).all()
    return jsonify(restaurant_list = [i.serialize for i in restaurants])

@app.route('/inspections/<restaurant_id>/JSON', methods=['GET'])
def restaurantInspectionJSON(restaurant_id):
    inspections = Inspections.query.filter_by(business_id=restaurant_id).order_by(desc(Inspections.date)).all()
    violations =  Violations.query.filter_by(business_id=restaurant_id).order_by(desc(Violations.date)).all()
    return jsonify(inspections = [i.serialize for i in inspections], violations = [i.serialize for i in violations])


@app.route('/')
def mainPage():
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form['Check'] == 'Check by id':
            restaurant_id = request.form['id']
            if restaurant_id:
                return redirect(url_for('restaurant', restaurant_id = restaurant_id))
        if request.form['Check'] == 'Check by name':
            restaurant_name = request.form['name']
            if restaurant_name:
                return redirect(url_for('restaurant_name', name = str(restaurant_name)))

    return render_template('index.html')


@app.route('/restaurant/name/<name>', methods=['GET', 'POST'])
def restaurant_name(name):
    
    pre = preprocess(name) 
    r = db.session.query(Restaurant).filter_by(name = pre).subquery()
    ins = db.session.query(r.c.id.label('id'),
                           r.c.name.label('name'),
                           r.c.address.label('addr'),
                           r.c.postal_code.label('post'),
                           r.c.latitude.label('lat'),
                           r.c.longitude.label('lon'),
                           r.c.phone_number.label('phone'),
                           func.max(Inspections.date).label('date')).\
                           filter(Inspections.score != None).\
                           join(Inspections, Inspections.business_id==r.c.id).\
                           group_by(Inspections.business_id).subquery()

    inspections = db.session.query(ins.c.id.label('id'), 
                                   ins.c.name.label('name'),
                                   ins.c.addr.label('addr'),
                                   ins.c.post.label('post'),
                                   ins.c.lat.label('lat'),
                                   ins.c.lon.label('lon'),
                                   ins.c.phone.label('phone'),
                                   ins.c.date.label('date'), 
                                   Inspections.score.label('score')).\
                                   join(Inspections, Inspections.business_id==ins.c.id).\
                                   filter(Inspections.date==ins.c.date).\
                                   filter(Inspections.score != None).subquery()                             
    results = db.session.query(inspections.c.id.label('id'), 
                               inspections.c.name.label('name'),
                               inspections.c.addr.label('addr'),
                               inspections.c.post.label('post'),
                               inspections.c.lat.label('lat'),
                               inspections.c.lon.label('lon'),
                               inspections.c.phone.label('phone'),
                               inspections.c.date.label('date'),
                               inspections.c.score.label('score'),
                               func.count(Violations.business_id)).\
                               join(Violations, Violations.business_id==inspections.c.id).\
                               group_by(inspections.c.id).all()

    if request.method == "GET":
        if results ==[]:
            flash('Restaurant %s not found.' % name)
            return redirect(url_for('index'))
        return  render_template('restaurant_by_name.html', name = pre, data = [list(r) for r in results])
    else:
        return  redirect(url_for('index'))


    
@app.route('/restaurant/<restaurant_id>', methods=['GET', 'POST'])
def restaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant is None:
        flash('Restaurant %s not found.' % restaurant_id)
        return redirect(url_for('index'))
    ins = db.session.query(Inspections.business_id.label('id'), 
                           Inspections.score.label('score'), 
                           Inspections.date.label('date')).\
                           filter_by(business_id = restaurant_id).\
                           filter(Inspections.score != None).\
                           order_by(Inspections.date.desc()).limit(1).subquery()
    results = db.session.query(ins.c.id, 
                               ins.c.score, 
                               func.count(Violations.business_id).label('ct')).\
                               join(Violations, Violations.business_id==ins.c.id).\
                               group_by(ins.c.id).first()
    inspections = db.session.query(Inspections).filter_by(business_id=restaurant_id).order_by(desc(Inspections.date)).all()
    violations = db.session.query(Violations).filter_by(business_id=restaurant_id).order_by(desc(Violations.date)).all()
    if request.method == "GET":       
        if inspections == None:
            flash('No inspections record found for %s.' % restaurant_id)
            return redirect(url_for('index'))
        return render_template('inspections.html', restaurant = restaurant, inspections = inspections, violations = violations, results = list(results))
    else:
        return  redirect(url_for('index'))

@app.route('/details', methods = ['GET'])
def detail():
    return render_template('explanation.html')


@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    NAMES = db.session.query(Restaurant).all()
    return jsonify(json_list=[i.name for i in NAMES]) 



