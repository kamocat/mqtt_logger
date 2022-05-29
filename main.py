from fastapi import FastAPI
import sqlite
app = FastAPI()

from fastapi.staticfiles import StaticFiles


db = sqlite.db('waterwall.db')

@app.get("/api/topics/{name:path}")
async def get_topics(name: str):
    topics = db.search(name)
    return {"topics": topics}

@app.get("/api/points/{topic:path}")
async def get_points(topic:str, t:int=None, days:float=1):
    data = db.fetch(topic,end_date=t, days=days)
    return data

@app.get("/api/alert")
async def get_alerts():
    alerts = {'test':'this is a drill'}
    if (db.latest('bat/charger/charge')["value"] > 3):
        alerts["battery_charger"] = 'done'
    return alerts

app.mount("/", StaticFiles(directory="graph"), name="static")
