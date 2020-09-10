import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect
import datetime as dt
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

app= Flask(__name__)


@app.route("/")
def welcome():
    """10_ins flask with ORM"""
    """list all available routes."""
    return(
      f"All Available routes:<br>" 
      f"Precipitation: /api/v1.0/precipitation<br/>"
      f"Stations: /api/v1.0/stations<br/>"
      f"Temperture observations Yr: /api/v1.0/tobs<br/>"
      f"Temperture Obs start: /api/v1.0/<start><br/>"
      f"Temperture Obs end: /api/v1.0/<start>/<end><br/>"

    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)

    precip = session.query(measurement.date, measurement.prcp).all()
    session.close()

    #precip_dates = list(np.ravel(precip))
    precipitation = []
    for prep in precip:
        r={}
        r[prep[0]]= prep[1]
        precipitation.append(r)
    return jsonify(precipitation)
@app.route('/api/v1.0/stations')
def route():
    session = Session(engine)
    results = session.query(station.station, station.name).all()
    session.close()
    stations = []
    for name in results:
        stat={}
        stat[name[0]]=name[1]
        stations.append(stat)
    return jsonify(stations)


    # stations = list(np.ravel(results))
    # return jsonify(stations)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    one_yr = dt.datetime.strptime(latest_date,"%Y-%m-%d")- dt.timedelta(days=365)
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_yr).all()
    
    session.close()
    tobs_lst =[]
    for date in query:
        tob={}
        tob['date']= date[0]
        tob['temperture']= date[1]
        tobs_lst.append(tob)
    return jsonify(tobs_lst)
@app.route('/api/v1.0/<start>')
def start_date(start):
    session= Session(engine)
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    session.close()
    
    meas = []
    for min,max, avg in results:
        tobs={}
        tobs['min']= min
        tobs['max']= max
        tobs['Average']= avg
        meas.append(tobs)
    return jsonify(meas)


@app.route('/api/v1.0/<start>/<end>')
def end_date(start,end):
    session= Session(engine)
    
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
       filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    
    stop = []
    for min,max, avg in results:
        start={}
        start['min']= min
        start['max']= max
        start['Average']= avg
        stop.append(start)
    return jsonify(stop)


if __name__=='__main__':
    app.run(debug=True)