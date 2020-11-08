import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        "hello"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    previous_date = dt.datetime(2016, 8, 23)

    prcp = session.query(func.avg(Measurement.prcp), Measurement.date).\
    filter(Measurement.date > previous_date).\
    group_by(Measurement.date).all()

    prcp_list = []

    for number, date in prcp:
        prcp_list.append({f"{date}": number})

    return (
        jsonify(prcp_list)
    )

@app.route("/api/v1.0/stations")
def stations():
    return (
        "hello"
    )

@app.route("/api/v1.0/tobs")
def tobs():
    return (
        "hello"
    )

@app.route("/api/v1.0/<start>")
def start():
    return (
        "hello"
    )

@app.route("/api/v1.0/<start>/<end>")
def end():
    return (
        "hello"
    )





if __name__ == '__main__':
    app.run(debug=True)