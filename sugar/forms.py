from flask_wtf import FlaskForm
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import Optional


class AddSugar(FlaskForm):
    sugar = IntegerField('Blood Sugar')
    date = DateField("Date")
    time = TimeField("Time")
    add_sugar = SubmitField("Add Sugar")


class AddDose(FlaskForm):
    dose = IntegerField("Dose")
    date = DateField("Date")
    time = TimeField("Time")
    add_dose = SubmitField("Add Dose")


class AddMeal(FlaskForm):
    meal = StringField("Meal")
    carbs = IntegerField("Carbs", validators=[Optional()])
    date = DateField("Date")
    time = TimeField("Time")
    add_meal = SubmitField("Add Meal")


class AddCarbs(FlaskForm):
    carbs = IntegerField("Carbs")
    submit = SubmitField("Add Carbs")
