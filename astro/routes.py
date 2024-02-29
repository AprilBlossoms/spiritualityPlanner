import requests
from flask import Blueprint, render_template, redirect, url_for, request
from datetime import date, datetime, timedelta

from flatlib import const, aspects
from flatlib.chart import Chart
from flatlib.datetime import Datetime

import config
from spiritualityPlanner import db
from spiritualityPlanner.astro.forms import AddTransitMeaning
from spiritualityPlanner.models import Day, Phase, Sign, Moonphase, Daychart, Tplanet, Nplanet, Transit, Aspect, \
    DayAspect

astro = Blueprint('astro', __name__, template_folder='templates', static_folder='static',
                  static_url_path='/astro/static')

BIRTH_CHART = Chart(config.BIRTHDATE, config.BIRTHPLACE, IDs=const.LIST_OBJECTS)
NATAL_SUN = BIRTH_CHART.get(const.SUN)
NATAL_MOON = BIRTH_CHART.get(const.MOON)
NATAL_MERCURY = BIRTH_CHART.get(const.MERCURY)
NATAL_VENUS = BIRTH_CHART.get(const.VENUS)
NATAL_MARS = BIRTH_CHART.get(const.MARS)
NATAL_JUPITER = BIRTH_CHART.get(const.JUPITER)
NATAL_SATURN = BIRTH_CHART.get(const.SATURN)
NATAL_URANUS = BIRTH_CHART.get(const.URANUS)
NATAL_NEPTUNE = BIRTH_CHART.get(const.NEPTUNE)
NATAL_PLUTO = BIRTH_CHART.get(const.PLUTO)

NATAL_PLANETS = [NATAL_SUN, NATAL_MOON, NATAL_MERCURY, NATAL_VENUS, NATAL_MARS, NATAL_JUPITER, NATAL_SATURN,
                 NATAL_URANUS, NATAL_NEPTUNE, NATAL_PLUTO]


class Aspect_Object():
    def __init__(self, aspect, natal_planet, transit_planet, transit_id, transit):
        self.aspect = aspect
        self.natal_planet = natal_planet
        self.transit_planet = transit_planet
        self.transit_id = transit_id
        self.transit = transit


@astro.route('/transits_today', methods=['GET', 'POST'])
def transits_today():
    day = Day.query.filter(Day.date == date.today()).first()
    form = AddTransitMeaning()
    formatted_date = date.today().strftime("%A, %B %d, %Y")
    if not day:
        date_str = date.today().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime('%H:%M:%S')
        day_date = date.today().strftime('%Y/%m/%d')
        day_datetime = Datetime(day_date, now_time, "-06:00")
        response = requests.get(
            f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{config.ZIPCODE}/{date_str}?unitGroup=us&key={config.WEATHER_API_KEY}&include=days&elements=moonphase')
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
        day_chart = Chart(day_datetime, config.LOCATION, IDs=const.LIST_OBJECTS)
        moon = day_chart.get(const.MOON)
        sun = day_chart.get(const.SUN)
        sun_sign = Sign.query.filter_by(sign=sun.sign).first()
        moon_sign = Sign.query.filter_by(sign=moon.sign).first()
        moonphase = Moonphase.query.filter_by(phase_id=phase_db.id, sign_id=moon_sign.id).first()

        day = Day(date=date.today(), moonphase_id=moonphase.id, sign_id=sun_sign.id)
        db.session.add(day)
        db.session.commit()
        chart = Daychart(chart=day_chart, day_id=day.id)
        db.session.add(chart)
        db.session.commit()
    else:
        chart = db.session.query(Daychart).filter_by(day_id=day.id).first()

    t_sun = chart.chart.get(const.SUN)
    t_moon = chart.chart.get(const.MOON)
    t_mercury = chart.chart.get(const.MERCURY)
    t_venus = chart.chart.get(const.VENUS)
    t_mars = chart.chart.get(const.MARS)
    t_jupiter = chart.chart.get(const.JUPITER)
    t_saturn = chart.chart.get(const.SATURN)
    t_uranus = chart.chart.get(const.URANUS)
    t_neptune = chart.chart.get(const.NEPTUNE)
    t_pluto = chart.chart.get(const.PLUTO)

    transit_planets = [t_sun, t_moon, t_mercury, t_venus, t_mars, t_jupiter, t_saturn, t_uranus, t_neptune, t_pluto]

    current_aspects = []
    sun_aspects = []
    moon_aspects = []
    merc_aspects = []
    venus_aspects = []
    mars_aspects = []
    jup_aspects = []
    sat_aspects = []
    uranus_aspects = []
    nep_aspects = []
    pluto_aspects = []
    for transit_planet in transit_planets:
        for natal_planet in NATAL_PLANETS:
            natal_planet_db = Nplanet.query.filter_by(planet=natal_planet.id).first()
            transit_planet_db = Tplanet.query.filter_by(planet=transit_planet.id).first()
            aspect = aspects.getAspect(transit_planet, natal_planet, const.MAJOR_ASPECTS)
            if aspect.type != -1 and aspect.orb < 2.6:
                if aspect.type == 0:
                    aspect_type = 'Conjunction'
                elif aspect.type == 60:
                    aspect_type = 'Sextile'
                elif aspect.type == 90:
                    aspect_type = 'Square'
                elif aspect.type == 120:
                    aspect_type = 'Trine'
                else:
                    aspect_type = "Opposition"
                relationship = Aspect.query.filter_by(aspect_type=aspect_type).first()
                transit = Transit.query.filter_by(nplanet_id=natal_planet_db.id, aspect_id=relationship.id,
                                                  tplanet_id=transit_planet_db.id).first()
                if transit_planet == t_sun:
                    sun_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_moon:
                    moon_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_mercury:
                    merc_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_venus:
                    venus_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_mars:
                    mars_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_jupiter:
                    jup_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_saturn:
                    sat_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_uranus:
                    uranus_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                        transit_planet=transit_planet, transit_id=transit.id,
                                                        transit=transit))
                if transit_planet == t_neptune:
                    nep_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))
                if transit_planet == t_pluto:
                    pluto_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                       transit_planet=transit_planet, transit_id=transit.id,
                                                       transit=transit))
                current_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                     transit_planet=transit_planet, transit_id=transit.id,
                                                     transit=transit))

                new_aspect = DayAspect(day_id=day.id, transit_id=transit.id)
                if DayAspect.query.filter_by(day_id=day.id, transit_id=transit.id).first() is None:
                    db.session.add(new_aspect)
                    db.session.commit()
    return render_template('transits_today.html', date=date, transit_planets=transit_planets,
                           sun_aspects=sun_aspects, chart=chart.chart, formatted_date=formatted_date,
                           moon_aspects=moon_aspects, merc_aspects=merc_aspects, venus_aspects=venus_aspects,
                           mars_aspects=mars_aspects, jup_aspects=jup_aspects, sat_aspects=sat_aspects,
                           uranus_aspects=uranus_aspects, nep_aspects=nep_aspects, pluto_aspects=pluto_aspects,
                           form=form)


@astro.route('/transits_upcoming')
def transits_upcoming():
    class Weekday:
        def __init__(self, formatted_date, id, chart, sun_aspects, moon_aspects, merc_aspects, venus_aspects, mars_aspects,
                     jup_aspects, sat_aspects, uranus_aspects, nep_aspects, pluto_aspects):
            self.formatted_date = formatted_date
            self.id = id
            self.chart = chart
            self.sun_aspects = sun_aspects
            self.moon_aspects = moon_aspects
            self.merc_aspects = merc_aspects
            self.venus_aspects = venus_aspects
            self.mars_aspects = mars_aspects
            self.jup_aspects = jup_aspects
            self.sat_aspects = sat_aspects
            self.uranus_aspects = uranus_aspects
            self.nep_aspects = nep_aspects
            self.pluto_aspects = pluto_aspects

    form = AddTransitMeaning()
    today = date.today()
    weekday = today.isoweekday()
    # The start of the week
#    start = today - timedelta(days=weekday)
    # build a simple range
    dates = [today + timedelta(days=d) for d in range(7)]
#    dates = [day.strftime('%Y-%m-%d') for day in dates]
    weekdays = []
    i = 1
    for item in dates:
        day = Day.query.filter(Day.date == item).first()
        formatted_date = item.strftime("%A, %B %d, %Y")
        if not day:
            date_str = item.strftime("%Y-%m-%d")
            now_time = datetime.now().strftime('%H:%M:%S')
            day_date = item.strftime('%Y/%m/%d')
            day_datetime = Datetime(day_date, now_time, "-06:00")
            response = requests.get(
                f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{config.ZIPCODE}/{date_str}?unitGroup=us&key={config.WEATHER_API_KEY}&include=days&elements=moonphase')
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
            day_chart = Chart(day_datetime, config.LOCATION, IDs=const.LIST_OBJECTS)
            moon = day_chart.get(const.MOON)
            sun = day_chart.get(const.SUN)
            sun_sign = Sign.query.filter_by(sign=sun.sign).first()
            moon_sign = Sign.query.filter_by(sign=moon.sign).first()
            moonphase = Moonphase.query.filter_by(phase_id=phase_db.id, sign_id=moon_sign.id).first()

            day = Day(date=date.today(), moonphase_id=moonphase.id, sign_id=sun_sign.id)
            db.session.add(day)
            db.session.commit()
            chart = Daychart(chart=day_chart, day_id=day.id)
            db.session.add(chart)
            db.session.commit()
        else:
            chart = db.session.query(Daychart).filter_by(day_id=day.id).first()
        week_id = i
        i += 1
        t_sun = chart.chart.get(const.SUN)
        t_moon = chart.chart.get(const.MOON)
        t_mercury = chart.chart.get(const.MERCURY)
        t_venus = chart.chart.get(const.VENUS)
        t_mars = chart.chart.get(const.MARS)
        t_jupiter = chart.chart.get(const.JUPITER)
        t_saturn = chart.chart.get(const.SATURN)
        t_uranus = chart.chart.get(const.URANUS)
        t_neptune = chart.chart.get(const.NEPTUNE)
        t_pluto = chart.chart.get(const.PLUTO)

        transit_planets = [t_sun, t_moon, t_mercury, t_venus, t_mars, t_jupiter, t_saturn, t_uranus, t_neptune, t_pluto]

        current_aspects = []
        sun_aspects = []
        moon_aspects = []
        merc_aspects = []
        venus_aspects = []
        mars_aspects = []
        jup_aspects = []
        sat_aspects = []
        uranus_aspects = []
        nep_aspects = []
        pluto_aspects = []
        for transit_planet in transit_planets:
            for natal_planet in NATAL_PLANETS:
                natal_planet_db = Nplanet.query.filter_by(planet=natal_planet.id).first()
                transit_planet_db = Tplanet.query.filter_by(planet=transit_planet.id).first()
                aspect = aspects.getAspect(transit_planet, natal_planet, const.MAJOR_ASPECTS)
                if aspect.type != -1 and aspect.orb < 2.6:
                    if aspect.type == 0:
                        aspect_type = 'Conjunction'
                    elif aspect.type == 60:
                        aspect_type = 'Sextile'
                    elif aspect.type == 90:
                        aspect_type = 'Square'
                    elif aspect.type == 120:
                        aspect_type = 'Trine'
                    else:
                        aspect_type = "Opposition"
                    relationship = Aspect.query.filter_by(aspect_type=aspect_type).first()
                    transit = Transit.query.filter_by(nplanet_id=natal_planet_db.id, aspect_id=relationship.id,
                                                      tplanet_id=transit_planet_db.id).first()
                    if transit_planet == t_sun:
                        sun_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                         transit_planet=transit_planet, transit_id=transit.id,
                                                         transit=transit))
                    if transit_planet == t_moon:
                        moon_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                          transit_planet=transit_planet, transit_id=transit.id,
                                                          transit=transit))
                    if transit_planet == t_mercury:
                        merc_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                          transit_planet=transit_planet, transit_id=transit.id,
                                                          transit=transit))
                    if transit_planet == t_venus:
                        venus_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                           transit_planet=transit_planet, transit_id=transit.id,
                                                           transit=transit))
                    if transit_planet == t_mars:
                        mars_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                          transit_planet=transit_planet, transit_id=transit.id,
                                                          transit=transit))
                    if transit_planet == t_jupiter:
                        jup_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                         transit_planet=transit_planet, transit_id=transit.id,
                                                         transit=transit))
                    if transit_planet == t_saturn:
                        sat_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                         transit_planet=transit_planet, transit_id=transit.id,
                                                         transit=transit))
                    if transit_planet == t_uranus:
                        uranus_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                            transit_planet=transit_planet, transit_id=transit.id,
                                                            transit=transit))
                    if transit_planet == t_neptune:
                        nep_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                         transit_planet=transit_planet, transit_id=transit.id,
                                                         transit=transit))
                    if transit_planet == t_pluto:
                        pluto_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                           transit_planet=transit_planet, transit_id=transit.id,
                                                           transit=transit))
                    current_aspects.append(Aspect_Object(aspect=aspect, natal_planet=natal_planet,
                                                         transit_planet=transit_planet, transit_id=transit.id,
                                                         transit=transit))

                    new_aspect = DayAspect(day_id=day.id, transit_id=transit.id)
                    if DayAspect.query.filter_by(day_id=day.id, transit_id=transit.id).first() is None:
                        db.session.add(new_aspect)
                        db.session.commit()

        weekdays.append(Weekday(formatted_date=formatted_date, id=week_id, chart=chart, sun_aspects=sun_aspects,
                                moon_aspects=moon_aspects, merc_aspects=merc_aspects,
                                venus_aspects=venus_aspects, mars_aspects=mars_aspects,
                                jup_aspects=jup_aspects, sat_aspects=sat_aspects,
                                uranus_aspects=uranus_aspects, nep_aspects=nep_aspects,
                                pluto_aspects=pluto_aspects))

    return render_template('transits_upcoming.html', date=date, weekdays=weekdays, form=form)


@astro.route('/addTransitMeaning/<transit_id>', methods=['GET', 'POST'])
def addTransitMeaning(transit_id):
    transit = Transit.query.filter_by(id=transit_id).first()
    transit.meaning = request.form['meaning']
    db.session.commit()
    return redirect(url_for('astro.transits_upcoming'))
