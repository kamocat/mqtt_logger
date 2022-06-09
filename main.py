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

app.mount("/", StaticFiles(directory="graph",html=True), name="static")
