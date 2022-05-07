from fastapi import FastAPI
import sqlite
app = FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount("/graph", StaticFiles(directory="graph"), name="static")

db = sqlite.db('test.db')

@app.get("/topics/{name:path}")
async def get_topics(name: str):
    topics = db.search(name)
    return {"topics": topics}

@app.get("/points/{topic:path}")
async def get_points(topic:str, t:int=None, span:int=60*60*24):
    data = db.fetch(topic,end_date=t, timespan=span)
    return data
