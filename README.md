# NucRadar v1 — SQLite prototype

This is a minimal, laptop-friendly prototype of the "Bloomberg for nuclear" terminal.
It uses **SQLite** (a single `.sqlite` file) and **Streamlit** for the UI.

## Contents

- `nuc_radar.sqlite` — (created by you) the local database file
- `db/schema_sqlite.sql` — DB schema
- `db/seed_companies_sqlite.sql` — initial company list
- `etl/config.yaml` — list of companies for ETL
- `etl/fetch_news.py` — dummy ETL that creates one test event per company
- `db.py` — SQLite helper for the app
- `app/app.py` — main Streamlit entrypoint
- `app/pages/` — Streamlit multipage views
- `requirements.txt` — Python dependencies

## Setup (Mac or Windows)

1. **Create a virtual environment and install deps**

   ```bash
   cd nuc_radar_sqlite_v1
   python -m venv .venv
   source .venv/bin/activate      # Windows: .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create the SQLite database and seed companies**

   ```bash
   sqlite3 nuc_radar.sqlite < db/schema_sqlite.sql
   sqlite3 nuc_radar.sqlite < db/seed_companies_sqlite.sql
   ```

3. **Run the ETL once to generate dummy events**

   ```bash
   python etl/fetch_news.py
   ```

   This will create one "Test milestone" event per company so the dashboard has data.

4. **Launch the Streamlit app**

   ```bash
   streamlit run app/app.py
   ```

   Your browser should open to `http://localhost:8501`.

## What you get

- **Overview Dashboard** — latest events + simple activity heat chart
- **Company Detail** — per-company event timeline
- **Events Log** — filterable list of events
- **Manual Entry** — add events by hand for testing

## Next steps (when you’re ready)

- Replace the dummy `fetch_articles_for_company()` in `etl/fetch_news.py`
  with a real news API integration.
- Add more fields (e.g., HALEU dependency, reactor class, geography).
- Extend scoring and tagging for "BS vs real" milestones.
