import streamlit as st
import db
from datetime import datetime, date

st.set_page_config(page_title="Admin Manual Entry", layout="centered")
st.title("Manual Event Entry")

companies = db.fetchall("SELECT id, name FROM companies ORDER BY name")
if not companies:
    st.warning("No companies found. Did you load the seed SQL?")
    st.stop()

company_map = {row["name"]: row["id"] for row in companies}
company_name = st.selectbox("Company", list(company_map.keys()))
company_id = company_map[company_name]

title = st.text_input("Title")
description = st.text_area("Description")
url = st.text_input("URL")
event_type = st.selectbox("Event type", ["fundraise","gov_program","regulatory","hardware","marketing"])
signal_level = st.slider("Signal level", 1, 5, 3)
amount = st.number_input("Amount (USD)", min_value=0.0, step=1.0)
ts_date = st.date_input("Event date", date.today())
ts_time = st.time_input("Event time", datetime.now().time())
ts_str = datetime.combine(ts_date, ts_time).isoformat()

if st.button("Save event"):
    db.execute(
        """INSERT INTO events
             (company_id, ts, title, description, url,
              event_type, signal_level, amount_usd)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (company_id, ts_str, title, description, url or None,
         event_type, int(signal_level), float(amount) if amount else None),
    )
    st.success("Event saved.")
