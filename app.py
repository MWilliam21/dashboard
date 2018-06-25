# import necessary libraries
import numpy as np
import re

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, Load,load_only,deferred,defer
from sqlalchemy import create_engine, func, column

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# @TODO: Setup your database here
engine=create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
BBu_otu=Base.classes.otu
Sample_db=Base.classes.samples
Meta=Base.classes.samples_metadata
session=Session(engine)
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/names")
def list_names():
    results= Sample_db.__table__.columns.keys()
    results.pop(0)
    data={
        "Names":results
    }
    return jsonify(data)

@app.route("/otu")
def types():
    results= session.query(BBu_otu.lowest_taxonomic_unit_found).all()
    data=list(np.ravel(results))
    
   
    return jsonify(data)

@app.route('/metadata')
def info():
    results=session.query(Meta.SAMPLEID,Meta.ETHNICITY,Meta.GENDER,Meta.AGE,Meta.BBTYPE,Meta.LOCATION,Meta.WFREQ).all()
    data=[]
    for res in results:
        data.append({
            "Age":res[0],
            "BBTYPE":res[1],
            "Ethnicity":res[2],
            "Gender":res[3],
            "Location":res[4],
            "Sample ID":res[5],
            "wFREQ":res[6]
        })
    return jsonify(data)

@app.route('/wfreq/<sample>')
def freq(sample):
    x=sample.split("_")[1]
    freq=[]
    results=session.query(Meta.WFREQ).filter(Meta.SAMPLEID==x).all()
    for res in results:
        freq.append({
            "Sample":x,
            "Wfreq":res[0]
        })
    return jsonify(freq)

@app.route('/samples/<sample>')
def getinfo(sample):
    result=session.query(Sample_db).options(load_only("otu_id",sample)).order_by(getattr(Sample_db,sample).desc()).filter(getattr(Sample_db,sample)>0).all()
    otus=[]
    sample_values=[]
    for res in result:
        otus.append(res.otu_id)
        sample_values.append(getattr(res,sample))

    data={
        "Otu_ID":otus,
        "Sample Values":sample_values
    }
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
