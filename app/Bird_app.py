import os
import json
import geojson
from geojson import FeatureCollection, Feature, Point
import pandas as pd
import numpy as np
from flask import Flask, render_template, jsonify

# path constructor
def path_constructor(parent, child):
    return os.path.join(parent, child)

# data folder
dataFolder = path_constructor("static", "data")
jsonFolder=path_constructor(dataFolder,"json")
csvFolder=path_constructor(dataFolder,"csv")
jsonFiles = os.listdir(jsonFolder)

# bird dataframe
bird_df = pd.read_csv(path_constructor(csvFolder, "bird_calls.csv"))
birdID = bird_df.fname.str[-10:-4]
birdList=list(np.unique(bird_df.label))


def openFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data=json.load(f)
    return data

def birdData(data, birdID):
    datalist = []
    for b in birdID:
        for i in range(len(data['recordings'])):
            if b == data["recordings"][i]["id"]:
                temp=data['recordings'][i]
                datalist.append(temp)
    return datalist


pathlist=[]
for file in jsonFiles:
    path=path_constructor(jsonFolder, file)
    pathlist.append(path)


birdDict={}
for path, bird in zip(pathlist,birdList):
    data=openFile(path)
    blist=birdData(data, birdID)
    birdDict[bird]=blist

    
def geoBird(chickList):
    bird_keys = ['id', 'en', 'gen', 'sp', 'cnt','loc', 'file', 'date']
    properties=[]
    coordinates = []
    geo = []
    for i in range(len(chickList)):
        prop={k:v for (k,v) in chickList[i].items() if k in bird_keys}
        properties.append(prop)
        lat = chickList[i]["lat"]        
        lng = chickList[i]["lng"]
        if lat != None and lng != None:
            coordinates.append((float(lng),float(lat)))   
            
    for pt, prop in zip(coordinates, properties):
        mypoint=Point(pt)
        geo.append(Feature(properties=prop, geometry=mypoint))
    
    feature_collection=FeatureCollection(geo)

    return feature_collection


geojsonData={}
for k in birdDict.keys():
    geojsonData[k]=geoBird(birdDict[k])

# Build flask app and routes

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("/index.html")

# American_Goldfinch
@app.route("/api/American_Goldfinch")
def goldfinch():
    DataBird = jsonify(geojsonData["American_Goldfinch"])
    return DataBird

# American_Robin
@app.route("/api/American_Robin")
def robin():
    DataBird = jsonify(geojsonData["American_Robin"])
    return DataBird

# Barn_Swallow
@app.route("/api/Barn_Swallow")
def barn():
    DataBird = jsonify(geojsonData["Barn_Swallow"])
    return DataBird

# Blue_Jay
@app.route("/api/Blue_Jay")
def jay():
    DataBird = jsonify(geojsonData["Blue_Jay"])
    return DataBird

# Blue-grey_Gnatcatcher
@app.route("/api/Blue-grey_Gnatcatcher")
def grey():
    DataBird = jsonify(geojsonData["Blue-grey_Gnatcatcher"])
    return DataBird

# Carolina_Chickadee
@app.route("/api/Carolina_Chickadee")
def chicka():
    DataBird = jsonify(geojsonData["Carolina_Chickadee"])
    return DataBird

# Carolina_Wren
@app.route("/api/Carolina_Wren")
def wren():
    DataBird = jsonify(geojsonData["Carolina_Wren"])
    return DataBird

# Cedar_Waxwing
@app.route("/api/Cedar_Waxwing")
def cedar():
    DataBird = jsonify(geojsonData["Cedar_Waxwing"])
    return DataBird

# Northern_Cardinal
@app.route("/api/Northern_Cardinal")
def cardinal():
    DataBird = jsonify(geojsonData["Northern_Cardinal"])
    return DataBird

# Ruby-crowned_Kinglet
@app.route("/api/Ruby-crowned_Kinglet")
def ruby():
    DataBird = jsonify(geojsonData["Ruby-crowned_Kinglet"])
    return DataBird
    

if __name__ == "__main__":
    app.run(debug=True, port = 8000)

