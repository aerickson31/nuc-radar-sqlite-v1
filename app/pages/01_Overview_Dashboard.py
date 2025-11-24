import streamlit as st
import pandas as pd
import db

st.set_page_config(page_title="Overview", layout="wide")
st.title("Overview Dashboard")

rows = db.fetchall(
    """SELECT e.ts,
                  c.name AS company,
                  e.title,
                  e.event_type,
                  e.signal_level
           FROM events e
           JOIN companies c ON e.company_id = c.id
           ORDER BY e.ts DESC
           LIMIT 50"""
)

if rows:
    df = pd.DataFrame(rows, columns=["ts","company","title","event_type","signal_level"])
    st.subheader("Latest events")
    st.dataframe(df)
else:
    st.info("No events yet. Run `python etl/fetch_news.py` to generate dummy events.")

rows = db.fetchall(
    """SELECT c.name AS company,
                  COUNT(*) AS event_count,
                  SUM(COALESCE(e.signal_level,0)) AS signal_sum
           FROM events e
           JOIN companies c ON e.company_id = c.id
           WHERE e.ts > datetime('now', '-90 days')
           GROUP BY c.name
           ORDER BY signal_sum DESC"""
)

if rows:
    heat_df = pd.DataFrame(rows, columns=["company","event_count","signal_sum"])
    st.subheader("Activity heat (last 90 days)")
    st.bar_chart(heat_df.set_index("company")["signal_sum"])
else:
    st.info("No recent activity to plot yet.")
