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
        f"hello! Welcome to my SQLAlchemy Challenge Website!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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
    station_list = session.query(Station.station).all()
    return (
        jsonify(station_list)
    )

@app.route("/api/v1.0/tobs")
def tobs():
    previous_date = dt.datetime(2016, 8, 23)
    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > previous_date).all()
    return (
        jsonify(tobs)
    )

@app.route("/api/v1.0/<start>")
def start_date_only(start):
    date = start.datetime(start)
    min_tobs = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date <= date).all()
    avg_tobs = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date <= date).all()
    max_tobs = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date <= date).all()

    return (
        f"The Minimum Tempurature on {date} was {min_tobs}</br>"
        f"The Average Tempurature on {date} was {avg_tobs}</br>"
        f"The Maximum Tempurature on {date} was {max_tobs}</br>"
    )

@app.route("/api/v1.0/<start>/<end>")
def end():
    return (
        "hello"
    )





if __name__ == '__main__':
    app.run(debug=True)