# app/main.py
from fastapi import FastAPI

from app import database, models
from app.tle_fetcher import fetch_and_store_tles

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/fetch-tles")
def fetch_tles():
    fetch_and_store_tles()
    return {"message": "TLEs fetched and stored."}
