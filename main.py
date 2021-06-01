import os

from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

import config
from db_client import get_temp_for_location, NoData, NoSuchLocation


class WeatherForm(FlaskForm):
    location = StringField("Location", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Find")


app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


@app.route("/", methods=["GET", "POST"])
def main_form():
    form = WeatherForm()

    if form.validate_on_submit():
        return redirect(
            "/weather?location={}&date={}".format(
                form.location.data, form.date.data.isoformat()
            )
        )

    return render_template("main.jinja", title="Weather History", form=form)


@app.route("/weather")
def get_weather_history():
    location = request.args.get("location")
    date = request.args.get("date")

    try:
        temp = get_temp_for_location(location, date)
        return render_template(
            "weather_history.jinja", location=location, date=date, temp=temp
        )
    except (NoData, NoSuchLocation) as e:
        return render_template("weather_history.jinja", error=e)
