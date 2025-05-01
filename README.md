
# 🛰️ Satellite Collision Predictor (WIP)

A full-stack application that predicts potential **satellite collisions** by fetching live orbital data (TLEs), simulating future orbits using orbital mechanics, and detecting near-miss events. This project uses modern tools like **FastAPI**, **Skyfield**, and eventually **CesiumJS** for 3D visualization.

> 🚧 Currently in active development. Phase 1 (backend setup + live TLE fetch) is complete.

---

## 🚀 Motivation

With the increasing number of satellites and space debris in orbit, the probability of accidental collisions is rising. This project aims to build a **real-time collision predictor** that:
- Fetches live orbital data
- Simulates satellite motion using physics
- Detects close-approach events
- Displays alerts and 3D visualizations of orbits

---

## 📚 Tech Stack

### 🧠 Core Libraries
| Area                | Tool                  | Description |
|---------------------|-----------------------|-------------|
| Backend API         | FastAPI               | High-performance async API framework |
| Orbit Propagation   | Skyfield, sgp4        | TLE parsing & orbital physics |
| DB ORM              | SQLAlchemy            | Object-relational mapper for DB models |
| Background Jobs     | Celery (Planned)      | Periodic TLE fetching and simulation |
| Visualization       | CesiumJS, Plotly (WIP)| 3D Earth + orbit renderer |
| Database            | SQLite (PostgreSQL soon) | Stores satellite metadata and warnings |

---

## ✅ Completed Features (Phase 1)

### 🔧 Backend Setup with FastAPI
- REST API initialized with FastAPI
- Project structure modularized for scalability

### 🛰️ Live TLE Fetcher
- Fetches live satellite TLEs from [Celestrak](https://celestrak.com)
- Parses and stores data (satellite name + 2-line orbital elements) in database

### 🗃️ Database
- SQLite used for local development
- Easily swappable with PostgreSQL via SQLAlchemy

---

## 📂 Project Structure

```
sat-collision-predictor/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # SQLAlchemy DB models
│   ├── database.py        # DB engine + session
│   ├── tle_fetcher.py     # Fetches and parses TLEs
│   ├── routes/            # (Planned) API route modules
│
├── satellites.db          # SQLite database (auto-created)
├── requirements.txt       # Dependencies
├── README.md              # You're here
```

---

## ⚙️ Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/shivarag200701/sat-collision-predictor.git
cd sat-collision-predictor
```

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```

Open browser and visit or use tools like psotman and create a GET request to the below URL:
```
http://localhost:8000/fetch-tles
```

### ✅ Output:
```json
{
  "message": "TLEs fetched and stored."
}
```

---

## 🔍 How It Works (Phase 1)

1. **TLE Source:** Uses public Celestrak API  
   URL: `https://celestrak.com/NORAD/elements/gp.php?GROUP=active&FORMAT=tle`

2. **TLE Parsing:** TLEs are in blocks of 3 lines:
   - Line 1 → Satellite name  
   - Line 2, 3 → Orbital data 

3. **Database Entry:**
   Each TLE set is stored as a record in the `satellites` table:
   ```sql
   | id | name          | tle_line1 | tle_line2 |
   |----|---------------|-----------|-----------|
   | 1  | ISS (ZARYA)   | ...       | ...       |
   ```

---

## 📌 Next Phases (Planned)

### Phase 2 – Orbit Simulation Engine
- Use Skyfield to compute satellite positions at time intervals
- Simulate for the next 24–48 hours
- Store positions or stream to frontend

### Phase 3 – Collision Detection Engine
- Check pairwise distances between satellites
- Raise alerts when below collision threshold (e.g. < 5 km)

### Phase 4 – 3D Visualization Dashboard
- Render orbits in CesiumJS
- Interactive UI for searching, filtering, and highlighting at-risk satellites

### Phase 5 – Background Task Scheduler
- Automatically refresh TLEs every 6–12 hours
- Keep predictions up to date using Celery or APScheduler

---

## 📜 License

MIT License. Feel free to fork and use with attribution.

---

## 🙋‍♂️ Author

**Shiva Raghav** – [GitHub](https://github.com/shivarag200701) | [LinkedIn](https://www.linkedin.com/in/shiva-raghav/)

> *Passionate about building beautiful, intelligent, and impactful software. Ping me if you're working on space-tech, backend systems, or AI-enhanced apps.*

---

## 🌟 Star the Repo

If you find this project interesting, please consider ⭐ starring the repo.  
It motivates further development and helps others discover the project.
