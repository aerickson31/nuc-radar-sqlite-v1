import streamlit as st
import pandas as pd
import db

st.set_page_config(page_title="Company Detail", layout="wide")
st.title("Company Detail")

companies = db.fetchall("SELECT id, name FROM companies ORDER BY name")
if not companies:
    st.warning("No companies found. Did you run the seed SQL?")
    st.stop()

company_map = {row["name"]: row["id"] for row in companies}
selected_name = st.selectbox("Select a company", list(company_map.keys()))
company_id = company_map[selected_name]

info = db.fetchone(
    "SELECT name, slug, ticker, type, tech, website, notes FROM companies WHERE id = ?",
    (company_id,),
)

if info:
    st.subheader(info["name"])
    st.write(f"Type: {info['type'] or 'n/a'}")
    st.write(f"Tech: {info['tech'] or 'n/a'}")
    if info["website"]:
        st.markdown(f"[Website]({info['website']})")
    if info["notes"]:
        st.write(info["notes"])

rows = db.fetchall(
    """SELECT ts, title, event_type, signal_level, url
           FROM events
           WHERE company_id = ?
           ORDER BY ts DESC
           LIMIT 100""",
    (company_id,),
)

st.subheader("Recent events")
if not rows:
    st.info("No events recorded yet for this company.")
else:
    for r in rows:
        label = f"[{r['ts']}] {r['title']} ({r['event_type'] or 'n/a'}, s={r['signal_level'] or 0})"
        with st.expander(label):
            if r["url"]:
                st.markdown(f"[Source link]({r['url']})")
