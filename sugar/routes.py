from flask import Blueprint, render_template, flash, redirect, url_for, request
from datetime import datetime, timedelta, date
import requests
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime

import secret
from spiritualityPlanner import db
from spiritualityPlanner.models import Day, Phase, Sign, Moonphase, Daychart, Sugar, Dose, Meal
from spiritualityPlanner.sugar.forms import AddSugar, AddDose, AddMeal, AddCarbs

sugar = Blueprint('sugar', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/sugar/static')


@sugar.route('/record', methods=["GET", "POST"])
def record():
    sugar_form = AddSugar()
    dose_form = AddDose()
    meal_form = AddMeal()

    if sugar_form.add_sugar.data and sugar_form.validate():
        sugar = sugar_form.sugar.data
        date = sugar_form.date.data
        date_str = date.strftime("%Y-%m-%d")
        time = sugar_form.time.data
        formatted_date = date.strftime("%A, %B %d, %Y")
        day = Day.query.filter_by(date=date).first()

        if not day:
            now_time = datetime.now().strftime('%H:%M:%S')
            day_date = date.strftime('%Y/%m/%d')
            day_datetime = Datetime(day_date, now_time, "-06:00")
            response = requests.get(
                f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{secret.ZIPCODE}/{date_str}?unitGroup=us&key={secret.WEATHER_API_KEY}&include=days&elements=moonphase')
            phase_num = (response.json()['days'][0]['moonphase'])
            if phase_num == 0:
                phase = 'New'
            elif phase_num < .25:
                phase = 'Waxing Crescent'
            elif phase_num == .25:
                phase = 'First Quarter'
            elif phase_num < .5:
                phase = 'Waxing Gibbous'
            elif phase_num == .5:
                phase = 'Full'
            elif phase_num < .75:
                phase = 'Waning Gibbous'
            elif phase_num == .75:
                phase = 'Last Quarter'
            else:
                phase = 'Waning Crescent'

            phase_db = Phase.query.filter_by(phase=phase).first()
            day_chart = Chart(day_datetime, secret.LOCATION, IDs=const.LIST_OBJECTS)
            moon = day_chart.get(const.MOON)
            sun = day_chart.get(const.SUN)
            sun_sign = Sign.query.filter_by(sign=sun.sign).first()
            moon_sign = Sign.query.filter_by(sign=moon.sign).first()
            moonphase = Moonphase.query.filter_by(phase_id=phase_db.id, sign_id=moon_sign.id).first()

            day = Day(date=date, moonphase_id=moonphase.id, sign_id=sun_sign.id)
            db.session.add(day)
            chart = Daychart(chart=day_chart, day_id=day.id)
            db.session.add(chart)
            db.session.commit()

        new_sugar = Sugar(sugar=sugar, day_id=day.id, time=time)
        db.session.add(new_sugar)
        db.session.commit()

        flash(f'{sugar} added to {formatted_date} at {time}')
        return redirect(url_for('sugar.record'))


    if dose_form.add_dose.data and dose_form.validate():
        dose = dose_form.dose.data
        date = dose_form.date.data
        date_str = date.strftime("%Y-%m-%d")
        time = dose_form.time.data
        formatted_date = date.strftime("%A, %B %d, %Y")
        day = Day.query.filter_by(date=date).first()

        if not day:
            now_time = datetime.now().strftime('%H:%M:%S')
            day_date = date.strftime('%Y/%m/%d')
            day_datetime = Datetime(day_date, now_time, "-06:00")
            response = requests.get(
                f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{secret.ZIPCODE}/{date_str}?unitGroup=us&key={secret.WEATHER_API_KEY}&include=days&elements=moonphase')
            phase_num = (response.json()['days'][0]['moonphase'])
            if phase_num == 0:
                phase = 'New'
            elif phase_num < .25:
                phase = 'Waxing Crescent'
            elif phase_num == .25:
                phase = 'First Quarter'
            elif phase_num < .5:
                phase = 'Waxing Gibbous'
            elif phase_num == .5:
                phase = 'Full'
            elif phase_num < .75:
                phase = 'Waning Gibbous'
            elif phase_num == .75:
                phase = 'Last Quarter'
            else:
                phase = 'Waning Crescent'

            phase_db = Phase.query.filter_by(phase=phase).first()
            day_chart = Chart(day_datetime, secret.LOCATION, IDs=const.LIST_OBJECTS)
            moon = day_chart.get(const.MOON)
            sun = day_chart.get(const.SUN)
            sun_sign = Sign.query.filter_by(sign=sun.sign).first()
            moon_sign = Sign.query.filter_by(sign=moon.sign).first()
            moonphase = Moonphase.query.filter_by(phase_id=phase_db.id, sign_id=moon_sign.id).first()

            day = Day(date=date, moonphase_id=moonphase.id, sign_id=sun_sign.id)
            db.session.add(day)
            chart = Daychart(chart=day_chart, day_id=day.id)
            db.session.add(chart)
            db.session.commit()

        new_dose = Dose(dose=dose, day_id=day.id, time=time)
        db.session.add(new_dose)
        db.session.commit()

        flash(f'{dose} units added to {formatted_date} at {time}')
        return redirect(url_for('sugar.record'))

    if meal_form.add_meal.data and meal_form.validate():
        meal = meal_form.meal.data
        date = meal_form.date.data
        date_str = date.strftime("%Y-%m-%d")
        time = meal_form.time.data
        carbs = meal_form.carbs.data
        formatted_date = date.strftime("%A, %B %d, %Y")
        day = Day.query.filter_by(date=date).first()

        if not day:
            now_time = datetime.now().strftime('%H:%M:%S')
            day_date = date.strftime('%Y/%m/%d')
            day_datetime = Datetime(day_date, now_time, "-06:00")
            response = requests.get(
                f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{secret.ZIPCODE}/{date_str}?unitGroup=us&key={secret.WEATHER_API_KEY}&include=days&elements=moonphase')
            phase_num = (response.json()['days'][0]['moonphase'])
            if phase_num == 0:
                phase = 'New'
            elif phase_num < .25:
                phase = 'Waxing Crescent'
            elif phase_num == .25:
                phase = 'First Quarter'
            elif phase_num < .5:
                phase = 'Waxing Gibbous'
            elif phase_num == .5:
                phase = 'Full'
            elif phase_num < .75:
                phase = 'Waning Gibbous'
            elif phase_num == .75:
                phase = 'Last Quarter'
            else:
                phase = 'Waning Crescent'

            phase_db = Phase.query.filter_by(phase=phase).first()
            day_chart = Chart(day_datetime, secret.LOCATION, IDs=const.LIST_OBJECTS)
            moon = day_chart.get(const.MOON)
            sun = day_chart.get(const.SUN)
            sun_sign = Sign.query.filter_by(sign=sun.sign).first()
            moon_sign = Sign.query.filter_by(sign=moon.sign).first()
            moonphase = Moonphase.query.filter_by(phase_id=phase_db.id, sign_id=moon_sign.id).first()

            day = Day(date=date, moonphase_id=moonphase.id, sign_id=sun_sign.id)
            db.session.add(day)
            chart = Daychart(chart=day_chart, day_id=day.id)
            db.session.add(chart)
            db.session.commit()

        new_meal = Meal(meal=meal, day_id=day.id, time=time)
        if carbs:
            new_meal.carbs = carbs
        else:
            new_meal.carbs = 0
        db.session.add(new_meal)
        db.session.commit()

        flash(f'{meal} added to {formatted_date} at {time}')
        return redirect(url_for('sugar.record'))
    return render_template('record.html', sugar_form=sugar_form, meal_form=meal_form,
                           dose_form=dose_form)


@sugar.route('/review', methods=["GET", "POST"])
def review():
    days = Day.query.filter(Day.date > date.today() - timedelta(weeks=1)).all()
    sugars = []
    doses = []
    meals = []
    for day in days:
        for sugar in day.sugars:
            sugars.append(sugar)
        for dose in day.doses:
            doses.append(dose)
        for meal in day.meals:
            meals.append(meal)

    form = AddCarbs()

    sugars = sorted(sugars, key=lambda sugar: (sugar.day.date, sugar.time))
    doses = sorted(doses, key=lambda dose: (dose.day.date, dose.time))
    meals = sorted(meals, key=lambda meal: (meal.day.date, meal.time))
    return render_template('review.html', sugars=sugars, doses=doses, meals=meals, form=form)


@sugar.route('/updateCarbs/<meal_id>', methods=['POST'])
def updateCarbs(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    carbs = request.form['carbs']
    meal.carbs = int(carbs)
    db.session.commit()
    flash(f'{meal.meal} carbs updated to {carbs}')
    return redirect(url_for('sugar.review'))
