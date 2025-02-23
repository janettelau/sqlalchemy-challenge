# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # Find the most recent date in the data set
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date_str = most_recent_date[0]

    # Calculate the date one year from the last date in data set
    one_year_ago = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d") - dt.timedelta(days=365)
    one_year_ago = one_year_ago.date()

    # Query for the last 12 months of precipitation data and scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Convert query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query to get the list of stations
    results = session.query(Station.station).all()

    session.close()

    # Convert the results into a list of stations
    stations = [station[0] for station in results]

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations from the previous year"""
    # Query the most active stations and their counts in descending order
    most_active_stations = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count().desc()).all()
    
    # Find the most recent date in the data set
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date_str = most_recent_date[0]

    # Calculate the date one year from the last date in data set
    one_year_ago = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d") - dt.timedelta(days=365)
    
    # Query the last 12 months of temperature observation data for this station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_stations[0][0]).\
        filter(Measurement.date >= one_year_ago - dt.timedelta(days=1)).all()
    
    session.close()

    # Convert the results into a list of dictionaries with date and temperature
    temperature_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of min, average, and max temperatures for a specfiic start"""
    # Query for the min, avg, and max temperatures from the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert the results into a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of min, average, and max temperatures for a specific start-end range, inclusive"""
    # Query for the min, avg, and max temperatures between the start and end date, inclusive
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert the results into a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)