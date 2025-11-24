import streamlit as st
import pandas as pd
import db

st.set_page_config(page_title="Events Log", layout="wide")
st.title("Events Log")

event_type = st.selectbox(
    "Filter by type",
    ["all","fundraise","gov_program","regulatory","hardware","marketing"]
)

params = []
query = """SELECT e.ts,
                    c.name AS company,
                    e.event_type,
                    e.signal_level,
                    e.title,
                    e.url
             FROM events e
             JOIN companies c ON e.company_id = c.id"""

if event_type != "all":
    query += " WHERE e.event_type = ?"
    params.append(event_type)

query += " ORDER BY e.ts DESC LIMIT 200"

rows = db.fetchall(query, params)
if rows:
    df = pd.DataFrame(rows, columns=["ts","company","event_type","signal_level","title","url"])
    st.dataframe(df)
else:
    st.info("No events to display yet.")
