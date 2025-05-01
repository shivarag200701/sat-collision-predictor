# app/tle_fetcher.py
import requests

from app.database import SessionLocal
from app.models import Satellite

CELESTRAK_URL = "https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"


def fetch_and_store_tles():
    db = SessionLocal()
    response = requests.get(CELESTRAK_URL)
    data = response.text.strip().split("\n")

    for i in range(0, len(data), 3):
        name = data[i].strip()
        tle1 = data[i + 1].strip()
        tle2 = data[i + 2].strip()

        sat = Satellite(name=name, tle_line1=tle1, tle_line2=tle2)
        db.add(sat)

    db.commit()
    db.close()
