#Importing the Directories needed 
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd 

#creating the Flask
app = Flask(__name__)

#creating the Homepage
@app.route("/")
def home(): 
    return(
        f"Available Routes:<br/> <br/>"
        f"Precipitation<br/> <br/>"
        f"Stations<br/> <br/>"
        f"Tobs<br/> <br/>"
        f"Start: <br/> <br/>"
        f"Start_End: <br/> <br/>"
    )

#Creating, Naming and Uploading the Database and Classes to be used 
engine = create_engine("sqlite:///./hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with = engine)
print(Base.classes.keys())
print(pd.read_sql_table(table_name = "measurement", con = engine).columns)
Measurement = Base.classes.measurement
Station = Base.classes.station 

#creating the /api/v1.0/precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation_route():
    session = Session(engine)
    session.close()
    start_date = '2016-08-23'
    return jsonify([{"Date": x[0], "Precipitation": x[1]} for x in session.
                                query(Measurement.date, Measurement.prcp).\
                                filter(Measurement.date >= start_date).\
                                order_by(Measurement.date) .\
                                all() ])
#creating the /api/v1.0/stations page
@app.route("/api/v1.0/stations")
def stations_route():
        session = Session(engine)
        session.close()
        return jsonify([x[0] for x in session.query(Measurement.station).distinct()])

#creating the /api/v1.0/tobs page
@app.route("/api/v1.0/tobs")
def tobs_route():
    session = Session(engine)
    start_date = '2016-08-23'
    session.close()
    return jsonify([{"Date": x[0], "Temperature": x[1]} for x in session. 
                                query(Measurement.date, Measurement.tobs).\
                                filter(Measurement.date >= start_date, Measurement.station == "USC00519281").\
                                order_by(Measurement.date).\
                                all() ])

#creating the /api/v1.0/start page
@app.route("/api/v1.0/start")
def start():
    session = Session(engine)
    start_date = '2016-08-23'
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    temp_data = []
    for tobs in results:
        temp_dict = {}
        temp_dict["Average"] = results[0][0]
        temp_dict["Minimum"] = results[0][1]
        temp_dict["Maximum"] = results[0][2]
        temp_data.append(temp_dict)

    session.close()
    return jsonify(temp_data)

#creating the /api/v1.0/start_end page
@app.route("/api/v1.0/start_end")
def temps_start_end():
    session = Session(engine)
    start_date = '2016-08-23'
    end_date = '2016-08-24'
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter((Measurement.date >= start_date)&(Measurement.date <= end_date)).\
        all()

    temp_data = []
    for tobs in results:
        temp_dict = {}
        temp_dict["Average"] = results[0][0]
        temp_dict["Minimum"] = results[0][1]
        temp_dict["Maximum"] = results[0][2]
        temp_data.append(temp_dict)

    session.close()
    return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug = True)
