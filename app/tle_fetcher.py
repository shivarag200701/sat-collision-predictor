# app/tle_fetcher.py
from datetime import datetime, timedelta

import requests

from app.database import SessionLocal
from app.models import Satellite, TLEMetadata

CELESTRAK_URL = "https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"


def extract_norad_id(tle_line1: str) -> int:
    return int(tle_line1[2:7].strip())


def fetch_and_store_tles():
    db = SessionLocal()
    try:
        # ✅ Step 1: Check last fetched time
        meta = db.query(TLEMetadata).first()
        now = datetime.utcnow()

        if meta and (now - meta.last_fetched_at) < timedelta(hours=6):
            print("⏳ Skipping TLE fetch – already fetched within last 6 hours.")
            return

        # ✅ Step 2: Fetch from CelesTrak
        print("📡 Fetching TLEs from CelesTrak...")
        response = requests.get(CELESTRAK_URL)
        data = response.text.strip().split("\n")

        count = 0
        for i in range(0, len(data), 3):
            try:
                name = data[i].strip()
                tle1 = data[i + 1].strip()
                tle2 = data[i + 2].strip()
                norad_id = extract_norad_id(tle1)

                sat = db.query(Satellite).filter(Satellite.norad_id == norad_id).first()

                if sat:
                    sat.name = name
                    sat.tle_line1 = tle1
                    sat.tle_line2 = tle2
                    print(f"🔁 Updating: {name} ({norad_id})")
                else:
                    sat = Satellite(
                        norad_id=norad_id, name=name, tle_line1=tle1, tle_line2=tle2
                    )
                    db.add(sat)
                    print(f"🆕 Inserting: {name} ({norad_id})")

                count += 1
            except Exception as e:
                print(f"❌ Error processing lines {i}-{i+2}: {e}")
                continue

        # ✅ Step 3: Update or insert fetch metadata
        if meta:
            meta.last_fetched_at = now
        else:
            meta = TLEMetadata(last_fetched_at=now)
            db.add(meta)

        db.commit()
        print(
            f"✅ Fetched and updated {count} satellites. Last fetch: {now.isoformat()}"
        )

    except Exception as e:
        print(f"🔥 Global TLE fetch error: {e}")
    finally:
        db.close()
