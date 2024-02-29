from spiritualityPlanner import db
from sqlalchemy.ext.associationproxy import association_proxy


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    moonphase_id = db.Column(db.Integer, db.ForeignKey('moonphase.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    tasks = db.relationship('Task', backref='day', lazy='dynamic')
    journals = db.relationship('Journal', backref='day', lazy='dynamic')
    gratitude = db.Column(db.Text)
    charts = db.relationship('Daychart', backref='day', lazy='dynamic')
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'))
    aspect_association = db.relationship('DayAspect', back_populates='day')
    aspects = association_proxy('aspect_association', 'transit')
    sugars = db.relationship('Sugar', backref='day', lazy='dynamic')
    doses = db.relationship('Dose', backref='day', lazy='dynamic')
    meals = db.relationship('Meal', backref='day', lazy='dynamic')


class Moonphase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id'))
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'))
    prompts = db.relationship('Prompt', backref='moonphase', lazy='dynamic')
    days = db.relationship('Day', backref='moonphase', lazy='dynamic')
    meaning = db.Column(db.Text)


class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.String(20))
    theme = db.Column(db.String(50))
    moonphases = db.relationship('Moonphase', backref='phase', lazy='dynamic')


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suit_id = db.Column(db.Integer, db.ForeignKey('suit.id'))
    number_id = db.Column(db.Integer, db.ForeignKey('number.id'))
    meaning = db.Column(db.Text)
    keywords = db.Column(db.String(50))
    img_path = db.Column(db.String(50))
    card_association = db.relationship('CardSign', back_populates='card')
    signs = association_proxy('card_association', 'card')
    decks = db.relationship('DeckCard', back_populates='card')


class Suit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suit = db.Column(db.String(15))
    theme = db.Column(db.Text)
    cards = db.relationship('Card', backref='suit', lazy='dynamic')


class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    theme = db.Column(db.Text)
    cards = db.relationship('Card', backref='number', lazy='dynamic')


class CardSign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column('card_id', db.Integer, db.ForeignKey('card.id'))
    sign_id = db.Column('sign_id', db.Integer, db.ForeignKey('sign.id'))
    meaning = db.Column(db.Text)
    prompts = db.relationship('Prompt', backref='card_sign', lazy='dynamic')

    card = db.relationship('Card', back_populates='card_association')
    sign = db.relationship('Sign', back_populates='cards')


class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text)
    moonphase_id = db.Column(db.Integer, db.ForeignKey('moonphase.id'), nullable=True)
    journals = db.relationship('Journal', backref='prompt', lazy=True)
    card_sign_id = db.Column(db.Integer, db.ForeignKey('card_sign.id'), nullable=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    done = db.Column(db.Boolean, default=0)

    def __str__(self):
        return self.task


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    journal_type = db.Column(db.String(15))
    entry = db.Column(db.Text)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=True)
    written_date = db.Column(db.Date)
    read = db.Column(db.Boolean, default=1)


class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sign = db.Column(db.String(20))
    theme = db.Column(db.Text)
    moonphases = db.relationship('Moonphase', backref='sign', lazy=True)
    cards = db.relationship('CardSign', back_populates='sign')
    days = db.relationship('Day', backref='sign', lazy='dynamic')
    transit_planets = db.relationship('Tplanet', backref='sign', lazy='dynamic')
    natal_planets = db.relationship('Nplanet', backref='sign', lazy='dynamic')


class Daychart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart = db.Column(db.PickleType)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))


class Tplanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(15))
    transits = db.relationship('Transit', backref='transit_planet', lazy='dynamic')
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'))
    img_path = db.Column(db.String(50))


class Nplanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(15))
    transits = db.relationship('Transit', backref='natal_planet', lazy='dynamic')
    sign_id = db.Column(db.Integer, db.ForeignKey('sign.id'))
    img_path = db.Column(db.String(50))


class Aspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aspect_type = db.Column(db.String(20))
    meaning = db.Column(db.Text)
    transits = db.relationship('Transit', backref='aspect', lazy='dynamic')


class Transit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nplanet_id = db.Column(db.Integer, db.ForeignKey('nplanet.id'))
    tplanet_id = db.Column(db.Integer, db.ForeignKey('tplanet.id'))
    aspect_id = db.Column(db.Integer, db.ForeignKey('aspect.id'))
    meaning = db.Column(db.Text)
    day_association = db.relationship('DayAspect', back_populates='transit')
    days = association_proxy('day_association', 'day')


class DayAspect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column('day_id', db.Integer, db.ForeignKey('day.id'))
    transit_id = db.Column('transit_id', db.Integer, db.ForeignKey('transit.id'))
    notes = db.Column(db.Text)

    day = db.relationship('Day', back_populates='aspect_association')
    transit = db.relationship('Transit', back_populates='day_association')





class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    img_path = db.Column(db.String(50))
    card_association = db.relationship('DeckCard', back_populates='deck')
    cards = association_proxy('card_association', 'card')


class DeckCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    name = db.Column(db.String(20))
    img_path = db.Column(db.String(50))
    description = db.Column(db.Text)
    auth_meaning = db.Column(db.Text)
    pers_meaning = db.Column(db.Text)
    deck = db.relationship('Deck', back_populates='card_association')
    card = db.relationship('Card', back_populates='decks')


class Sugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sugar = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    time = db.Column(db.Time)


class Dose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dose = db.Column(db.Integer)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    time = db.Column(db.Time)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(30))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    time = db.Column(db.Time)
    carbs = db.Column(db.Integer)
