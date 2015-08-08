from flask import render_template, flash, redirect, session, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from datetime import datetime
from app import app, db
from .forms import LoginForm, EditForm
from .models import Restaurant, Inspections, Violations
from sqlalchemy import desc
from sqlalchemy.orm import load_only

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import string

def preprocess(s):
    s = s.strip()
    return string.capwords(s)

#NAMES=["abc","abcd","abcde","abcdef", "cde"]

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
    restaurant = db.session.query(Restaurant).filter_by(name = pre).all()
    if request.method == "GET":
        if restaurant ==[]:
            flash('Restaurant %s not found.' % name)
            return redirect(url_for('index'))
        SFmap = Map(identifier="view-side", lat=SFgeo[0], lng=SFgeo[1], style="height:400px;width:480px;margin:10;", markers=[(restaurant[i].latitude, restaurant[i].longitude) for i in range(len(restaurant))])
        return  render_template('restaurant_by_name.html', name = pre, data = restaurant, SFmap = SFmap)
    else:
        return  redirect(url_for('index'))


    
@app.route('/restaurant/<restaurant_id>', methods=['GET', 'POST'])
def restaurant(restaurant_id):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
    if restaurant is None:
        flash('Restaurant %s not found.' % restaurant_id)
        return redirect(url_for('index'))

    inspections = db.session.query(Inspections).filter_by(business_id=restaurant_id).order_by(desc(Inspections.date)).all()
    violations = db.session.query(Violations).filter_by(business_id=restaurant_id).order_by(desc(Violations.date)).all()
    if request.method == "GET":       
        if inspections == None:
            flash('No inspections record found for %s.' % restaurant_id)
            return redirect(url_for('index'))
        return render_template('inspections.html', id = restaurant_id, name = restaurant.name, inspections = inspections, violations = violations)
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



